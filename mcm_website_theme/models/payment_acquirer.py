# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time
from odoo import api, fields, models,_


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    code=fields.Char("Code")
    instalment=fields.Boolean('Instalement',default=False)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', "code déja existe !"),
    ]

    def set_amount(self,instalement,auth="public"):
            payment = self.env['payment.acquirer'].sudo().search([('code', 'ilike', 'stripe')])
            if instalement:
                if payment:
                    payment.instalment=True
            else:
                payment.instalment = False
    def render(self, reference, amount, currency_id, partner_id=False, values=None):

        transaction = self.env['payment.transaction'].sudo().search([('reference', 'ilike', reference)])
        self.done_msg=_('Bravo ! Commande confirmée \n Vous allez recevoir dans quelques minutes un mail ! Pas de mail reçu ? Vérifiez dans vos courriers indésirables ou spams.')
        for rec in self:
            data = reference.split("-")
            sale = self.env['sale.order'].sudo().search([('name', 'ilike', data[0])])
            amount_before_instalment=amount
            if rec.instalment and amount>1000:
                amount=amount/3
                if transaction:
                    transaction.amount = transaction.amount / 3
                if sale:
                    sale.amount_total = sale.amount_total / 3
            self.instalment=False
        result = super(PaymentAcquirer, self).render(reference, amount, currency_id, partner_id, values)
        sale.amount_total = amount_before_instalment
        return result




