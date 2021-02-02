# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    mcm_paid_amount = fields.Monetary(string='Montant payé',compute='_get_mcm_paid_amount',store=True)
    acompte_invoice = fields.Boolean(default=False)
    pourcentage_acompte = fields.Integer("Pourcentage d'acompte")
    module_id=fields.Many2one('mcmacademy.module','Module')
    session_id=fields.Many2one('mcmacademy.session','Session')
    pricelist_id=fields.Many2one('product.pricelist','Liste de prix')
    cpf_solde_invoice = fields.Boolean(default=False)
    cpf_acompte_invoice=fields.Boolean(default=False)
    cpf_acompte_amount= fields.Monetary('Montant acompte')



    @api.depends('amount_total', 'amount_residual')
    def _get_mcm_paid_amount(self):
        for rec in self:
            payments = self.env['account.payment'].search(['|',('communication', "=", rec.name),('communication', 'like', rec.invoice_origin)])
            paid_amount = 0.0

            for payment in payments:
                communication=str(payment.communication)
                communication = communication.split("-")
                if payment.company_id==rec.company_id and payment.state=="posted" and payment.communication in [communication,rec.name]:
                    paid_amount += payment.amount
            rec.mcm_paid_amount = paid_amount

    # def unlink(self):
    #     for move in self:
    #         move.line_ids.unlink()
    #     for rec in self:
    #         rec.unlink()
    #     return super(AccountMove, self).unlink()
