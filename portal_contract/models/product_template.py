# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Session(models.Model):
    _inherit = 'product.template'

    product_details_ids=fields.One2many('product.template.details','product_tmpl_id','Description')
    formation_price=fields.Monetary('Prix Formation',compute='_compute_price_formation',store=True)


    @api.depends('product_details_ids')
    def _compute_price_formation(self):
        for rec in self:
            if rec.product_details_ids:
                total_price = 0
                for product in rec.product_details_ids:
                    total_price=total_price+product.price
                rec.formation_price=total_price