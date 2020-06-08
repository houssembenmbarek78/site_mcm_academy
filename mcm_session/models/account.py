# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import AccessError, UserError, ValidationError
from addons.payment.controllers.portal import PaymentProcessing
from datetime import datetime, timedelta, date
from datetime import datetime, timedelta, date

class AccountPayment(models.Model):
    _inherit = "account.payment"


    def _payment_stripe_3X(self):
        invoices=self.env['account.move'].sudo().search([('invoice_payment_state', '=', 'not_paid'), ('type', '=', 'out_invoice')])
        # stripe.api_key = "sk_test_z5yAyGCO7UQ0lrS8RZNsL8kE00evWDCsu7"
        if invoices:
            for invoice in invoices:
                order=self.env['sale.order'].sudo().search([('name', 'ilike', invoice.invoice_origin)])
                pm_id=self.env['payment.token'].sudo().search([('partner_id', '=', invoice.partner_id.id)])[-1].id
                first_payment_date = invoice.create_date + timedelta(days=30)
                second_payment_date = invoice.create_date + timedelta(days=60)
                first_payment_date = first_payment_date.date()
                second_payment_date = second_payment_date.date()
                # if(str(date.today())==str(first_payment_date) or str(date.today())==str(second_payment_date)):

                acquirer = self.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
                vals = {}
                vals.update({
                    'acquirer_id': acquirer.id,
                    'amount': invoice.amount_total / 3,
                    'currency_id': invoice.currency_id.id,
                    'partner_id': invoice.partner_id.id,
                    'sale_order_ids': [(6, 0, order.ids)],
                })
                tx = self.env['payment.transaction'].create(vals)
                tx.payment_token_id=pm_id
                res = tx._stripe_create_payment_intent()
                if (str(res.get('status'))=='succeeded'):

                    tx.acquirer_reference=res.get('id')
                    tx.date=datetime.now()
                    tx._set_transaction_done()
                    journal = self.env['account.journal'].sudo().search(
                        [('code', 'ilike', 'STRIP')])
                    payment_method = self.env['account.payment.method'].sudo().search(
                        [('code', 'ilike', 'electronic')])
                    acquirer = self.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
                    payment = self.env['account.payment'].create({'payment_type': 'inbound',
                                                                  'payment_method_id': payment_method.id,
                                                                  'partner_type': 'customer',
                                                                  'partner_id': invoice.partner_id.id,
                                                                  'amount': tx.amount,
                                                                  'currency_id': invoice.currency_id.id,
                                                                  'payment_date': datetime.now(),
                                                                  'journal_id': journal.id,
                                                                  'communication': tx.reference,
                                                                  'payment_token_id': pm_id,
                                                                  'invoice_ids': [(6, 0, invoice.ids)],
                                                                  })
                    payment.payment_transaction_id = tx
                    tx.payment_id=payment
                    payment.post()
                    vals = {
                        'partner_name': invoice.partner_id.name,
                        'category_id': self.env['helpdesk.ticket.category'].
                            sudo().search([('code', '=', 'account')]).id,
                        'partner_email': invoice.partner_id.email,
                        'description': 'Veuillez relancez le paiement de '+str(invoice.partner_id.name),
                        'name': 'Relance paiement ' + str(invoice.partner_id.name),
                        'attachment_ids': False,
                        'channel_id':
                            self.env['helpdesk.ticket.channel'].
                                sudo().search([('name', '=', 'Web')]).id,
                        'team_id': self.env['helpdesk.ticket.team'].sudo().search([('name', 'like', 'Compta')],
                                                                                  limit=1).id,
                        'invoice_id':invoice.id
                    }
                    new_ticket = self.env['helpdesk.ticket'].sudo().create(
                        vals)

class AccountMove(models.Model):
    _inherit = "account.move"

    def _create_payment_transaction(self, vals):
        '''Similar to self.env['payment.transaction'].create(vals) but the values are filled with the
        current invoices fields (e.g. the partner or the currency).
        :param vals: The values to create a new payment.transaction.
        :return: The newly created payment.transaction record.
        '''
        # Ensure the currencies are the same.
        currency = self[0].currency_id
        if any([inv.currency_id != currency for inv in self]):
            raise ValidationError(_('A transaction can\'t be linked to invoices having different currencies.'))

        # Ensure the partner are the same.
        partner = self[0].partner_id
        if any([inv.partner_id != partner for inv in self]):
            raise ValidationError(_('A transaction can\'t be linked to invoices having different partners.'))

        # Try to retrieve the acquirer. However, fallback to the token's acquirer.
        acquirer_id = vals.get('acquirer_id')
        acquirer = None
        payment_token_id = vals.get('payment_token_id')

        if payment_token_id:
            payment_token = self.env['payment.token'].sudo().browse(payment_token_id)

            # Check payment_token/acquirer matching or take the acquirer from token
            if acquirer_id:
                acquirer = self.env['payment.acquirer'].browse(acquirer_id)
                if payment_token and payment_token.acquirer_id != acquirer:
                    raise ValidationError(_('Invalid token found! Token acquirer %s != %s') % (
                    payment_token.acquirer_id.name, acquirer.name))
                if payment_token and payment_token.partner_id != partner:
                    raise ValidationError(_('Invalid token found! Token partner %s != %s') % (
                    payment_token.partner.name, partner.name))
            else:
                acquirer = payment_token.acquirer_id

        # Check an acquirer is there.
        if not acquirer_id and not acquirer:
            raise ValidationError(_('A payment acquirer is required to create a transaction.'))

        if not acquirer:
            acquirer = self.env['payment.acquirer'].browse(acquirer_id)

        # Check a journal is set on acquirer.
        if not acquirer.journal_id:
            raise ValidationError(_('A journal must be specified of the acquirer %s.' % acquirer.name))

        if not acquirer_id and acquirer:
            vals['acquirer_id'] = acquirer.id
        amount=sum(self.mapped('amount_residual'))
        if self.invoice_origin:
            order = self.env['sale.order'].sudo().search([('name', 'ilike', self.invoice_origin)])
            if order:
                if order.instalment and self.amount_total>1000:
                    amount=self.amount_total/3

        vals.update({
            'amount': amount,
            'currency_id': currency.id,
            'partner_id': partner.id,
            'invoice_ids': [(6, 0, self.ids)],
        })
        transaction = self.env['payment.transaction'].create(vals)

        # Process directly if payment_token
        if transaction.payment_token_id:
            transaction.s2s_do_transaction()

        return transaction
    def action_invoice_register_payment_stripe(self):
        for rec in self:
            order = self.env['sale.order'].sudo().search([('name', 'ilike', rec.invoice_origin)])
            pm_id = self.env['payment.token'].sudo().search([('partner_id', '=', rec.partner_id.id)])[-1].id
            acquirer = self.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
            vals = {}
            vals.update({
                'acquirer_id': acquirer.id,
                'amount': rec.amount_total / 3,
                'currency_id': rec.currency_id.id,
                'partner_id': rec.partner_id.id,
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
                                                              'partner_id': rec.partner_id.id,
                                                              'amount': tx.amount,
                                                              'currency_id': rec.currency_id.id,
                                                              'payment_date': datetime.now(),
                                                              'journal_id': journal.id,
                                                              'communication': tx.reference,
                                                              'payment_token_id': pm_id,
                                                              'invoice_ids': rec.ids,
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
            elif(str(res.get('status')) == 'requires_payment_method'):
                vals = {
                    'partner_name': rec.partner_id.name,
                    'category_id': self.env['helpdesk.ticket.category'].
                            sudo().search([('code', '=', 'account')]).id,
                    'partner_email': rec.partner_id.email,
                    'description': 'Retard de paiement,merci de contacter le stagiaire',
                    'name': 'Retard de paiement,Contacter '+str(rec.partner_id.name),
                    'attachment_ids': False,
                    'channel_id':
                        self.env['helpdesk.ticket.channel'].
                            sudo().search([('name', '=', 'Web')]).id,
                    'team_id': self.env['helpdesk.ticket.team'].sudo().search([('name', 'like', 'Compta')], limit=1).id
                }
                new_ticket = self.env['helpdesk.ticket'].sudo().create(
                    vals)
                message_id = self.env['message.wizard'].create({'message': _("Le paiement a été echoué....veuillez contacter le client")})
                return {
                    'name': _('Paiement echoué'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }





