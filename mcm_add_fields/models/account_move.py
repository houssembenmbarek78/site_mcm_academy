# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    mcm_paid_amount = fields.Monetary(string='Montant payé',compute='_get_mcm_paid_amount',store=True)

    @api.depends('amount_total','amount_residual')
    def _get_mcm_paid_amount(self):
        for rec in self:
            rec.mcm_paid_amount=rec.amount_total-rec.amount_residual

