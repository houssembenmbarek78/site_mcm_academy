# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError
from addons.payment.controllers.portal import PaymentProcessing
from datetime import datetime, timedelta, date
from datetime import datetime, timedelta, date


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _payment_stripe_3X(self):
        invoices = self.env['account.move'].sudo().search(
            [('invoice_payment_state', '=', 'not_paid'), ('type', '=', 'out_invoice'), ('state', '=', 'posted'),
             ('amount_total', '>', '1000'), ('type_facture', '=', 'web')])
        # stripe.api_key = "sk_test_z5yAyGCO7UQ0lrS8RZNsL8kE00evWDCsu7"
        # if invoices:
        #     for invoice in invoices:
        #         order = self.env['sale.order'].sudo().search([('name', 'ilike', invoice.invoice_origin)])
        #         pm_id = self.env['payment.token'].sudo().search([('partner_id', '=', invoice.partner_id.id)])[-1].id
        #         first_payment_date = invoice.create_date + timedelta(days=30)
        #         second_payment_date = invoice.create_date + timedelta(days=60)
        #         first_payment_date = first_payment_date.date()
        #         second_payment_date = second_payment_date.date()
        #         if (str(date.today()) == str(first_payment_date) or str(date.today()) == str(second_payment_date)):
        #
        #             acquirer = self.env['payment.acquirer'].sudo().search([('name', 'ilike', 'stripe'),('company_id',"=",invoice.company_id.id)])
        #             vals = {}
        #             vals.update({
        #                 'acquirer_id': acquirer.id,
        #                 'amount': invoice.amount_total / 3,
        #                 'currency_id': invoice.currency_id.id,
        #                 'partner_id': invoice.partner_id.id,
        #                 'sale_order_ids': [(6, 0, order.ids)],
        #             })
        #             tx = self.env['payment.transaction'].create(vals)
        #             tx.payment_token_id = pm_id
        #             res = tx._stripe_create_payment_intent()
        #             if (str(res.get('status')) == 'succeeded'):
        #                 tx.acquirer_reference = res.get('id')
        #                 tx.date = datetime.now()
        #                 tx._set_transaction_done()
        #                 journal = self.env['account.journal'].sudo().search(
        #                     [('code', 'ilike', 'STRIP')])
        #                 payment_method = self.env['account.payment.method'].sudo().search(
        #                     [('code', 'ilike', 'electronic')])
        #                 acquirer = self.env['payment.acquirer'].sudo().search([('name', 'ilike', 'stripe'),('company_id',"=",invoice.company_id.id)])
        #                 payment = self.env['account.payment'].create({'payment_type': 'inbound',
        #                                                               'payment_method_id': payment_method.id,
        #                                                               'partner_type': 'customer',
        #                                                               'partner_id': invoice.partner_id.id,
        #                                                               'amount': tx.amount,
        #                                                               'currency_id': invoice.currency_id.id,
        #                                                               'payment_date': datetime.now(),
        #                                                               'journal_id': journal.id,
        #                                                               'communication': tx.reference,
        #                                                               'payment_token_id': pm_id,
        #                                                               'invoice_ids': [(6, 0, invoice.ids)],
        #                                                               })
        #                 payment.payment_transaction_id = tx
        #                 tx.payment_id = payment
        #                 payment.post()
        #                 message_id = self.env['message.wizard'].create(
        #                     {'message': _("Le paiement a été effectué avec succès")})
        #                 return {
        #                     'name': _('Paiement avec succès'),
        #                     'type': 'ir.actions.act_window',
        #                     'view_mode': 'form',
        #                     'res_model': 'message.wizard',
        #                     # pass the id
        #                     'res_id': message_id.id,
        #                     'target': 'new'
        #                 }
        #             elif (str(res.get('status')) == 'requires_payment_method'):
        #
        #                 new_ticket = self.env['helpdesk.ticket'].sudo().create(
        #                     vals)
        #                 message_id = self.env['message.wizard'].create(
        #                     {'message': _("Le paiement a été echoué....veuillez contacter le client")})
        #                 return {
        #                     'name': _('Paiement echoué'),
        #                     'type': 'ir.actions.act_window',
        #                     'view_mode': 'form',
        #                     'res_model': 'message.wizard',
        #                     # pass the id
        #                     'res_id': message_id.id,
        #                     'target': 'new'
        #                 }
        #                 vals = {
        #                     'partner_email': invoice.partner_id.email,
        #                     'description': 'Veuillez relancez le paiement de ' + str(invoice.partner_id.name),
        #                     'name': 'Relance paiement ' + str(invoice.partner_id.name),
        #                     'team_id': self.env['helpdesk.team'].sudo().search([('name', 'like', 'Compta')],
        #                                                                        limit=1).id,
        #                     'invoice_id': invoice.id
        #                 }
        #                 new_ticket = self.env['helpdesk.ticket'].sudo().create(
        #                     vals)
        digimoov_invoices=self.env['account.move'].sudo().search(
            [('invoice_payment_state', '=', 'not_paid'), ('type', '=', 'out_invoice'), ('state', '=', 'posted'),
              ('type_facture', '=', 'web'),('company_id',"=",2)])
        print('digimoov_invoices')
        for invoice in digimoov_invoices:
            print(invoice)
            order = self.env['sale.order'].sudo().search([('name', 'ilike', invoice.invoice_origin)])
            pm_id = self.env['payment.token'].sudo().search([('partner_id', '=', invoice.partner_id.id)])[-1].id
            first_payment_date = invoice.create_date + timedelta(days=30)
            second_payment_date = invoice.create_date + timedelta(days=60)
            first_payment_date = first_payment_date.date()
            second_payment_date = second_payment_date.date()
            if (str(date.today()) == str(first_payment_date) or str(date.today()) == str(second_payment_date)):
                acquirer = self.env['payment.acquirer'].sudo().search([('name', 'ilike', 'stripe'),('company_id',"=",invoice.company_id.id)])
                vals = {}
                print(acquirer)
                journal = self.env['account.journal'].sudo().search(
                    [('type', "=", 'bank'), ('code', 'ilike', 'BNK')])
                if order.instalment and order.instalment_number>1:
                    vals.update({
                        'acquirer_id': acquirer.id,
                        'amount': invoice.amount_total / order.instalment_number,
                        'currency_id': invoice.currency_id.id,
                        'partner_id': invoice.partner_id.id,
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
                            [('type', "=", 'bank'),('code','ilike','BNK')])

                        payment_method = self.env['account.payment.method'].sudo().search(
                            [('code', 'ilike', 'electronic')])
                        acquirer = self.env['payment.acquirer'].sudo().search([('name', 'ilike', 'stripe'),('company_id',"=",invoice.company_id.id)])
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
                                                                      'company_id':invoice.company_id.id,
                                                                      'invoice_ids': [(6, 0, invoice.ids)],
                                                                      })
                        payment.payment_transaction_id = tx
                        tx.payment_id = payment
                        payment.post()
                elif (str(res.get('status')) == 'requires_payment_method'):
                    print('paiement echoué')





class AccountMove(models.Model):
    _inherit = "account.move"

    type_facture = fields.Selection(selection=[
        ('interne', 'En Interne'),
        ('web', 'Par le site web'),
    ], string='Facture générer')

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
        amount = sum(self.mapped('amount_residual'))
        if self.invoice_origin:
            order = self.env['sale.order'].sudo().search([('name', 'ilike', self.invoice_origin)])
            print('orderrrrr')
            print(order)
            print(self.company_id.id)
            print(order.instalment)
            if order:
                if order.instalment and self.amount_total > 1000 and self.company_id.id==1:
                    amount = self.amount_total / 3
                if order.instalment and self.company_id.id==2:
                    amount = self.amount_total / order.instalment_number

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
            if rec.amount_total  > 1000 and rec.type_facture=='web' and rec.company_id.id==1:
                order = self.env['sale.order'].sudo().search([('name', 'ilike', rec.invoice_origin)])
                pm_id = self.env['payment.token'].sudo().search([('partner_id', '=', rec.partner_id.id)])[-1].id
                acquirer = self.env['payment.acquirer'].sudo().search([('name', 'ilike', 'stripe'),('company_id',"=",rec.company_id.id)])
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
                    acquirer = self.env['payment.acquirer'].sudo().search([('name', 'ilike', 'stripe'),('company_id',"=",rec.company_id.id)])
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
                elif (str(res.get('status')) == 'requires_payment_method'):
                    vals = {
                        'partner_email': rec.partner_id.email,
                        'description': 'Retard de paiement,merci de contacter le stagiaire',
                        'name': 'Retard de paiement,Contacter ' + str(rec.partner_id.name),
                        'team_id': self.env['helpdesk.team'].sudo().search([('name', 'like', 'Compta')], limit=1).id
                    }
                    new_ticket = self.env['helpdesk.ticket'].sudo().create(
                        vals)
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

    def _get_move_display_name(self, show_ref=False):
        ''' Helper to get the display name of an invoice depending of its type.
        :param show_ref:    A flag indicating of the display name must include or not the journal entry reference.
        :return:            A string representing the invoice.
        '''
        self.ensure_one()
        draft_name = ''
        if self.state == 'draft':
            draft_name += {
                'out_invoice': _('Draft Invoice'),
                'out_refund': _('Draft Credit Note'),
                'in_invoice': _('Draft Bill'),
                'in_refund': _('Draft Vendor Credit Note'),
                'out_receipt': _('Draft Sales Receipt'),
                'in_receipt': _('Draft Purchase Receipt'),
                'entry': _('Draft Entry'),
            }[self.type]
            if not self.name or self.name == '/':
                draft_name += ' (* %s)' % str(self.id)
            else:
                draft_name += ' ' + self.name
        partner_name=''
        if self.partner_id:
            partner_name=self.partner_id.name
        invoice_name=''
        if self.type=='out_invoice':
            invoice_name='facture_'
        if self.type=='out_refund':
            invoice_name='Avoir_facture_'
        return(invoice_name)+(partner_name)+('_') + (draft_name or self.name) + (show_ref and self.ref and ' (%s%s)' % (self.ref[:50], '...' if len(self.ref) > 50 else '') or '')

    @api.model_create_multi
    def create(self, vals_list):
        if any('type_facture' in vals and vals.get('type_facture') == 'interne' and 'partner_id' in vals for vals in vals_list):
            for vals in vals_list:
                partner_id=vals.get('partner_id')
                partner=self.env['res.partner'].sudo().search([('id', '=', partner_id)], limit=1)
                if not partner.mcm_session_id and not partner.module_id:
                    raise UserError(_("Vous pouvez pas créer une facture car le client n'est pas encore lié avec une session et un module..veuillez le lier avec une session d'abord "))
        return super(AccountMove, self).create(vals_list)