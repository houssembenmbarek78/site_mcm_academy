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
        stripe=self.env['sale.order'].sudo().search(['|','&',('name', 'ilike', 'Stripe'),('code', 'ilike', 'stripe')])
        if (self.stripe_payment_intent and self.state == 'done'):
            list = []
            sale.partner_id.mcm_session_id=sale.partner_id.module_id.session_id
            for partner in sale.session_id.client_ids:
                list.append(partner.id)
            list.append(sale.partner_id.id)
            sale.session_id.write({'client_ids': [(6, 0, list)]})
            canceled_list=[]
            for partner in sale.session_id.panier_perdu_ids:
                if (partner.id != sale.partner_id.id):
                    canceled_list.append(partner.id)
            sale.session_id.write({'panier_perdu_ids': [(6, 0, canceled_list)]})
            sale.partner_id.statut='won'

