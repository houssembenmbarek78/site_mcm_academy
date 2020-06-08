# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, models, _, SUPERUSER_ID


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _set_transaction_done(self):
        transaction = super(PaymentTransaction, self)._set_transaction_done()

        data = self.reference.split("-")
        sale = self.env['sale.order'].sudo().search([('name', 'ilike', data[0])])
        if (self.stripe_payment_intent and self.state == 'done'):
            sale.action_confirm()
            moves = sale._create_invoices(final=True)
            sale.action_cancel()
            sale.sale_action_sent()
            Session = self.env['mcm.session']
            for order in sale.order_line:
                session = Session.sudo().search([('product_id', '=', order.product_id.product_tmpl_id.id)])
                if session:
                    sale.partner_id.session_id = session
            if sale.env.su:
                # sending mail in sudo was meant for it being sent from superuser
                sale = sale.with_user(SUPERUSER_ID)
            template_id = sale._find_mail_template(force_confirmation_template=True)
            if template_id:
                sale.with_context(force_send=True).message_post_with_template(template_id,
                                                                              composition_mode='comment',
                                                                              email_layout_xmlid="portal_contract.mcm_mail_notification_paynow_online")
            test=sale.get_portal_url(report_type='pdf', download=True)


    def _reconcile_after_transaction_done(self):
        transaction=super(PaymentTransaction,self)._reconcile_after_transaction_done()
        invoices = self.mapped('invoice_ids')
        template = self.env['mail.template'].sudo().search([('model', '=', 'account.move')])
        # template_id = self.env['ir.model.data'].xmlid_to_res_id('portal_contract.mcm_email_template_edi_invoice',
        #                                                         raise_if_not_found=False)

        for invoice in invoices.with_user(SUPERUSER_ID):
            invoice.message_post_with_template(int(template),
                                               composition_mode='comment',
                                               email_layout_xmlid="portal_contract.mcm_mail_notification_paynow_online")
