# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from datetime import datetime,date


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    invoice_id = fields.Many2one('account.move', 'Facture')

    @api.model_create_multi
    def create(self, list_value):
        tickets = super(HelpdeskTicket, self).create(list_value)
        message_type = self.env['mail.activity.type'].sudo().search([('name', 'ilike', _('À faire'))], limit=1)
        for ticket in tickets:
            if ticket.team_id:
                users = ticket.team_id.member_ids
                if users:
                    for user in users:
                        print('user')
                        print(user)
                        message = self.env['mail.activity'].sudo().create({
                            'activity_type_id': message_type.id,
                            'res_model_id': self.env['ir.model'].search([('model', '=', 'helpdesk.ticket')],
                                                                        limit=1).id,
                            'summary': 'nouveau ticket créer',
                            'date_deadline': date.today(),
                            'user_id': user.id,
                            'res_id': int(tickets),
                            'note': 'Un nouveau ticket reçu...veuillez la traiter',
                        })
        return tickets

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