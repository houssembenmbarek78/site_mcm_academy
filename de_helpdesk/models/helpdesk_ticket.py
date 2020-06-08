from odoo import _, api, fields, models, tools
from datetime import datetime, date

class HelpdeskTicket(models.Model):

    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _rec_name = 'number'
    _order = 'number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['helpdesk.ticket.stage'].search([], limit=1).id

    number = fields.Char(string='Ticket number', default="/",
                         readonly=True)
    name = fields.Char(string='Title', required=True)
    description = fields.Text(required=False)
    user_id = fields.Many2one('res.users', string='Assigned to', tracking=True, domain=lambda self: [('groups_id', 'in', self.env.ref('de_helpdesk.group_helpdesk_user').id)])

    user_ids = fields.Many2many(comodel_name='res.users',related='team_id.user_ids',string='Users')

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['helpdesk.ticket.stage'].search([])
        return stage_ids

    stage_id = fields.Many2one(
        'helpdesk.ticket.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        default=_get_default_stage_id,
        track_visibility='onchange',
    )
    partner_id = fields.Many2one('res.partner')
    partner_name = fields.Char()
    partner_email = fields.Char()

    last_stage_update = fields.Datetime(
        string='Last Stage Update',
        default=fields.Datetime.now,
    )
    assigned_date = fields.Datetime(string='Assigned Date')
    closed_date = fields.Datetime(string='Closed Date')
    closed = fields.Boolean(related='stage_id.closed')
    unattended = fields.Boolean(related='stage_id.unattended')
    tag_ids = fields.Many2many('helpdesk.ticket.tag')
    pole_emploi = fields.Char('Pole emploi')
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(
            'helpdesk.ticket')
    )
    channel_id = fields.Many2one(
        'helpdesk.ticket.channel',
        string='Channel',
        help='Channel indicates where the source of a ticket'
             'comes from (it could be a phone call, an email...)',
    )
    category_id = fields.Many2one('helpdesk.ticket.category',
                                  string='Category')
    team_id = fields.Many2one('helpdesk.ticket.team')
    priority = fields.Selection(selection=[
        ('0', _('Low')),
        ('1', _('Medium')),
        ('2', _('High')),
        ('3', _('Very High')),
    ], string='Priority', default='1')
    attachment_ids = fields.One2many(
        'ir.attachment', 'res_id',
        domain=[('res_model', '=', 'helpdesk.ticket')],
        string="Media Attachments")
    color = fields.Integer(string='Color Index')
    kanban_state = fields.Selection([
        ('normal', 'Default'),
        ('done', 'Ready for next stage'),
        ('blocked', 'Blocked')], string='Kanban State')
    active = fields.Boolean('Active', default=True)
    invoice_id = fields.Many2one('account.move', 'Facture')

    def send_user_mail(self):
        self.env.ref('de_helpdesk.assignment_email_template'). \
            send_mail(self.id)

    def restart_paiement(self):
        if self.invoice_id:
            order = self.env['sale.order'].sudo().search([('name', 'ilike', self.invoice_id.invoice_origin)])
            pm_id = self.env['payment.token'].sudo().search([('partner_id', '=', self.invoice_id.partner_id.id)])[-1].id
            acquirer = self.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
            vals = {}
            vals.update({
                'acquirer_id': acquirer.id,
                'amount': self.invoice_id.amount_total / 3,
                'currency_id': self.invoice_id.currency_id.id,
                'partner_id': self.invoice_id.partner_id.id,
                'type': 'form',
                'sale_order_ids': [(6, 0, order.ids)],
            })
            tx = self.env['payment.transaction'].create(vals)
            tx.payment_token_id = pm_id
            res = tx._stripe_create_payment_intent()
            if (str(res.get('status')) == 'succeeded'):
                tx.acquirer_reference = res.get('id')
                tx.date = datetime.now()
                tx._set_transaction_done()
                journal = self.env['account.journal'].sudo().search(
                    [('code', 'ilike', 'STRIP')])
                payment_method = self.env['account.payment.method'].sudo().search(
                    [('code', 'ilike', 'electronic')])
                acquirer = self.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
                payment = self.env['account.payment'].create({'payment_type': 'inbound',
                                                              'payment_method_id': payment_method.id,
                                                              'partner_type': 'customer',
                                                              'partner_id': self.invoice_id.partner_id.id,
                                                              'amount': tx.amount,
                                                              'currency_id': self.invoice_id.currency_id.id,
                                                              'payment_date': datetime.now(),
                                                              'journal_id': journal.id,
                                                              'communication': tx.reference,
                                                              'payment_token_id': pm_id,
                                                              'invoice_ids': self.invoice_id.ids,
                                                              })
                payment.payment_transaction_id = tx
                tx.payment_id = payment
                payment.post()
                message_id = self.env['message.wizard'].create({'message': _("Le paiement a été effectué avec succès")})
                return {
                    'name': _('Paiement avec succès'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }
            elif (str(res.get('status')) == 'requires_payment_method'):
                message_id = self.env['message.wizard'].create(
                    {'message': _("Le paiement a été echoué....veuillez contacter le client")})
                return {
                    'name': _('Paiement echoué'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }

    def assign_to_me(self):
        self.write({'user_id': self.env.user.id})

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_name = self.partner_id.name
            self.partner_email = self.partner_id.email

    #@api.onchange('team_id', 'user_id')
    #def _onchange_dominion_user_id(self):
        #if self.user_id:
         #   if self.user_id and self.user_ids and \
          #          self.user_id not in self.user_ids:
           #     self.update({
            #        'user_id': False
             #   })
              #  return {'domain': {'user_id': []}}
        #if self.team_id:
         #   return {'domain': {'user_id': [('id', 'in', self.user_ids.ids)]}}
        #else:
         #   return {'domain': {'user_id': []}}

    # ---------------------------------------------------
    # CRUD
    # ---------------------------------------------------

    @api.model
    def create(self, vals):
        if vals.get('number', '/') == '/':
            seq = self.env['ir.sequence']
            if 'company_id' in vals:
                seq = seq.with_context(force_company=vals['company_id'])
            vals['number'] = seq.next_by_code(
                'helpdesk.ticket.sequence') or '/'
        #res = super().create(vals)

        # context: no_log, because subtype already handle this
        tickets = super(HelpdeskTicket, self).create(vals)
        for ticket in tickets:
            if ticket.partner_id:
                ticket.message_subscribe(partner_ids=ticket.partner_id.ids)
            if ticket.partner_name:
                self.helpdesk_ticket_send_mail(ticket)
        # make customer follower
        #for ticket in tickets:
            #if ticket.partner_id:
                #ticket.message_subscribe(partner_ids=ticket.partner_id.ids)
                
        # Check if mail to the user has to be sent
        if vals.get('user_id') and tickets:
            tickets.send_user_mail()
        message_type = self.env['mail.activity.type'].sudo().search([('name', 'ilike', _('À faire'))], limit=1)
        admin = self.env['res.users'].sudo().search([('name', 'ilike', 'Administrator')], limit=1)
        for ticket in tickets:
            print('category')
            print(vals.get('category_id'))
            category_code = self.env['helpdesk.ticket.category'].search([('id', '=', vals.get('category_id'))],
                                                                        limit=1).code
            if (category_code == 'client' or category_code == 'presse'):
                team = self.env['helpdesk.ticket.team'].sudo().search([('name', 'like', 'Client')], limit=1)
                if team:
                    ticket.team_id = team.id
            if (category_code == 'account'):
                team = self.env['helpdesk.ticket.team'].sudo().search([('name', 'like', 'Compta')], limit=1)
                if team:
                    ticket.team_id = team.id
            if (category_code == 'partner'):
                team = self.env['helpdesk.ticket.team'].sudo().search([('name', 'like', 'Administration')], limit=1)
                if team:
                    ticket.team_id = team.id

        for ticket in tickets:
            if ticket.team_id:
                print('team_id')
                users = ticket.team_id.user_ids
                for user in users:
                    message = self.env['mail.activity'].sudo().create({
                        'activity_type_id': message_type.id,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'helpdesk.ticket')], limit=1).id,
                        'summary': 'nouveau ticket créer',
                        'date_deadline': date.today(),
                        'user_id': user.id,
                        'res_id': int(tickets),
                        'note': 'Un nouveau ticket reçu...veuillez la traiter',
                    })
            
        return tickets

    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "number" not in default:
            default['number'] = self.env['ir.sequence'].next_by_code(
                'helpdesk.ticket.sequence'
            ) or '/'
        res = super(HelpdeskTicket, self).copy(default)
        return res

    def write(self, vals):
        for ticket in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['helpdesk.ticket.stage'].browse(
                    [vals['stage_id']])
                vals['last_stage_update'] = now
                if stage_obj.closed:
                    vals['closed_date'] = now
            if vals.get('user_id'):
                vals['assigned_date'] = now

        res = super(HelpdeskTicket, self).write(vals)
        
        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])

        # Check if mail to the user has to be sent
        for ticket in self:
            if vals.get('user_id'):
                ticket.send_user_mail()
        return res

    # ---------------------------------------------------
    # Mail gateway
    # ---------------------------------------------------

    def _track_template(self, changes):
        res = super(HelpdeskTicket, self)._track_template(changes)
        test_task = self[0]
        #changes, tracking_value = tracking[test_task.id]
        if "stage_id" in changes and test_task.stage_id.mail_template_id:
            res['stage_id'] = (test_task.stage_id.mail_template_id,
                               {"composition_mode": "mass_mail"})

        return res

    @api.model
    def message_new(self, msg, custom_values=None):
        """ Override message_new from mail gateway so we can set correct
        default values.
        """
        if custom_values is None:
            custom_values = {}
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
            'description': msg.get('body'),
            'partner_email': msg.get('from'),
            'partner_id': msg.get('author_id')
        }
        defaults.update(custom_values)

        # Write default values coming from msg
        ticket = super().message_new(msg, custom_values=defaults)

        # Use mail gateway tools to search for partners to subscribe
        email_list = tools.email_split(
            (msg.get('to') or '') + ',' + (msg.get('cc') or '')
        )
        partner_ids = [p for p in ticket._find_partner_from_emails(
            email_list, force_create=False
        ) if p]
        ticket.message_subscribe(partner_ids)

        return ticket

    def message_update(self, msg, update_vals=None):
        """ Override message_update to subscribe partners """
        email_list = tools.email_split(
            (msg.get('to') or '') + ',' + (msg.get('cc') or '')
        )
        partner_ids = [p for p in self._find_partner_from_emails(
            email_list, force_create=False
        ) if p]
        self.message_subscribe(partner_ids)
        return super().message_update(msg, update_vals=update_vals)

    def message_get_suggested_recipients(self):
        recipients = super().message_get_suggested_recipients()

        for ticket in self:
            reason = _('Partner Email') \
                if ticket.partner_id and ticket.partner_id.email \
                else _('Partner Id')

            if ticket.partner_id and ticket.partner_id.email:
                ticket._message_add_suggested_recipient(
                    recipients,
                    partner=ticket.partner_id,
                    reason=reason
                )
            elif ticket.partner_email:
                ticket._message_add_suggested_recipient(
                    recipients,
                    email=ticket.partner_email,
                    reason=reason
                )
        return recipients

    def helpdesk_ticket_send_mail(self, ticket):
        template_id = self.env['ir.model.data'].xmlid_to_res_id('de_helpdesk.mcm_helpdesk_partner_email_template',
                                                                raise_if_not_found=False)
        if template_id:
            ticket.with_context(force_send=True).message_post_with_template(template_id,composition_mode='mass_mail')
