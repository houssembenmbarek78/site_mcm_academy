# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, models, _, SUPERUSER_ID


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _set_transaction_done(self):
        transaction = super(PaymentTransaction, self)._set_transaction_done()
        if self.reference:
            data = self.reference.split("-")
            sale = self.env['sale.order'].sudo().search([('name', 'ilike', data[0])])
            if (self.stripe_payment_intent and self.state == 'done' and sale):
                Session = self.env['mcm.session']
                sale.partner_id.mcm_session_id = sale.session_id
                sale.partner_id.module_id = sale.module_id
                for order in sale.order_line:
                    session = Session.sudo().search([('product_id', '=', order.product_id.product_tmpl_id.id)])
                    if session:
                        sale.partner_id.session_id = session
                if sale.env.su:
                    # sending mail in sudo was meant for it being sent from superuser
                    sale = sale.with_user(SUPERUSER_ID)
                template_id = sale._find_mail_template(force_confirmation_template=True)
                if template_id and sale:
                    sale.with_context(force_send=True).message_post_with_template(template_id,
                                                                                  composition_mode='comment',
                                                                                  email_layout_xmlid="portal_contract.mcm_mail_notification_paynow_online"
                                                                                 )
                if sale:
                    test=sale.get_portal_url(report_type='pdf', download=True)

    # Ce programme a été modifié par seifeddinne le 31/05/2021
    # ajout du champs methode_payment qui stock la valeur carte bleu si le payment et par carte bleu

    def _reconcile_after_transaction_done(self):
        transaction=super(PaymentTransaction,self)._reconcile_after_transaction_done()
        invoices = self.mapped('invoice_ids')
        template = self.env['mail.template'].sudo().search([('model', '=', 'account.move')])
        if self.reference:
            data = self.reference.split("-")
            sale = self.env['sale.order'].sudo().search([('name', 'ilike', data[0])])
            if (self.stripe_payment_intent and self.state == 'done' and sale):
                
                sale.action_confirm()
                sale.partner_id.mcm_session_id=sale.session_id
                sale.partner_id.module_id=sale.module_id
                moves = sale._create_invoices(final=False)
                for move in moves:
                    move.type_facture='web'
                    move.methodes_payment = 'cartebleu'
                    move.module_id=sale.module_id
                    move.session_id=sale.session_id
                    sale.partner_id.mcm_session_id = sale.session_id
                    sale.partner_id.module_id = sale.module_id
                    if sale.pricelist_id.code:
                        move.pricelist_id=sale.pricelist_id
                    move.company_id=sale.company_id
                    move.action_post()
                sale.action_cancel()
                sale.sale_action_sent()

                for move in moves.with_user(SUPERUSER_ID):
                    move.message_post_with_template(int(template),
                                                       composition_mode='comment',
                                                       email_layout_xmlid="portal_contract.mcm_mail_notification_paynow_online"
                                                      )
