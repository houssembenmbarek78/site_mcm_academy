import logging
import werkzeug
import odoo.http as http
import base64
import werkzeug
import requests
from odoo.http import request
_logger = logging.getLogger(__name__)


class HelpdeskTicketController(http.Controller):

    @http.route('/ticket/close', type="http", auth="user")
    def support_ticket_close(self, **kw):
        """Close the support ticket"""
        values = {}
        ticket_id=kw.get('ticket_id')
        stage_id=kw.get('stage_id')
        if ticket_id:
            print('ticket')
            print(ticket_id)
        if stage_id:
            print('stage_id')
            print(stage_id)
        ticket = http.request.env['helpdesk.ticket'].sudo().\
            search([('id', '=', int(ticket_id))])
        stage=http.request.env['helpdesk.ticket.stage'].sudo().\
            search([('id', '=', stage_id)])
        print(ticket)
        print(stage)
        # if ticket:
        #     ticket.stage_id=stage.id
        # ticket.sudo().write({'stage_id': int(stage_id)})
        # request.env['helpdesk.ticket'].browse(int(ticket_id)).sudo().write({'stage_id': int(stage_id)})
        product = request.env['helpdesk.ticket'].browse(int(ticket_id))
        if product:
            print(product)
            product.write({'stage_id': stage})
        return werkzeug.utils.redirect("/my/ticket/" + str(ticket.id))

    @http.route(['/new/ticket','/new/ticket/<string:pm>'], type="http", auth="public", website=True)
    def create_new_ticket(self,pm=None, **kw):
        categories = http.request.env['helpdesk.ticket.category']. \
            search([('active', '=', True)])
        public_user = http.request.env['res.users'].sudo().search([('id', '=', 4), ('active', '=', False)])
        if http.request.uid == public_user.id:
            name = ""
            email = ""
        else:
            name = http.request.env.user.name
            email = http.request.env.user.email
        if pm:
            pm = pm
        else:
            pm = ''
        # email = http.request.env.user.email
        # name = http.request.env.user.name
        return http.request.render('de_helpdesk.portal_create_ticket', {
            'categories': categories, 'email': email, 'name': name, 'pm':pm})

    @http.route('/submitted/ticket',
                type="http", auth="public", website=True, csrf=True)
    def submit_ticket(self, **kw):
        vals = {
            'partner_name': kw.get('name'),
            'pole_emploi': kw.get('emploi_id'),
            'company_id': http.request.env.user.company_id.id,
            'category_id': kw.get('category'),
            'partner_email': kw.get('email'),
            'description': kw.get('description'),
            'name': kw.get('subject'),
            'attachment_ids': False,
            'channel_id':
                request.env['helpdesk.ticket.channel'].
                sudo().search([('name', '=', 'Web')]).id,
            'partner_id':
                request.env['res.partner'].sudo().search([
                    ('name', '=', kw.get('name')),
                    ('email', '=', kw.get('email'))]).id
        }
        new_ticket = request.env['helpdesk.ticket'].sudo().create(
            vals)
        new_ticket.message_subscribe(
            partner_ids=request.env.user.partner_id.ids)
        if kw.get('attachment'):
            for c_file in request.httprequest.files.getlist('attachment'):
                data = c_file.read()
                if c_file.filename:
                    request.env['ir.attachment'].sudo().create({
                        'name': c_file.filename,
                        'datas': base64.b64encode(data),
                        #'datas_fname': c_file.filename,
                        'res_model': 'helpdesk.ticket',
                        'res_id': new_ticket.id
                    })
        public_user = http.request.env['res.users'].sudo().search([('id', '=', 4), ('active', '=', False)])
        if http.request.uid == public_user.id:
            return werkzeug.utils.redirect("/success-ticket")
        if new_ticket.pole_emploi:
            last_order = http.request.env['sale.order'].sudo().search(
                [('partner_id', '=', new_ticket.partner_id.id), ('state', '=', 'draft')])[-1]
            session = last_order.session_id
            if session:
                last_order.partner_id.mcm_session_id = session
                list = []
                for partner in session.prospect_ids:
                    list.append(partner.id)
                list.append(new_ticket.partner_id.id)
                session.write({'prospect_ids': [(6, 0, list)]})
                canceled_list = []
                for partner in session.panier_perdu_ids:
                    if (partner.id != new_ticket.partner_id.id):
                        canceled_list.append(partner.id)
                session.write({'panier_perdu_ids': [(6, 0, canceled_list)]})
            new_ticket.partner_id.statut = 'indecis'
            last_order.unlink()
        return werkzeug.utils.redirect("/my/tickets")

    @http.route('/success-ticket', type="http", auth="public", website=True)
    def get_success_message(self, **kw):
        return http.request.render('de_helpdesk.success_ticket')
