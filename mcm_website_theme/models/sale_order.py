# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "sale.order"

    instalment_number=fields.Integer("Tranches",compute='get_instalment_number')
    amount_to_pay=fields.Monetary('Montant à Payer',compute='compute_amount_to_pay')
    instalment=fields.Boolean(default=False)

    @api.depends('amount_total')
    def get_instalment_number(self):
        for rec in self:
            if (rec.amount_total>1000):
                rec.instalment_number=3
            else:
                rec.instalment_number=1

    @api.depends('amount_total','instalment_number')
    def compute_amount_to_pay(self):
        for rec in self:
           rec.amount_to_pay=rec.amount_total/rec.instalment_number

    def sale_action_sent(self):
        return self.write({'state': 'sent'})


