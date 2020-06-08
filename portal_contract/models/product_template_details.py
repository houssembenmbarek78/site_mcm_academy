# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Session(models.Model):
    _name = 'product.template.details'

    name=fields.Char('Nom')
    price=fields.Monetary('Prix')
    formation_time=fields.Char('temps de formation')
    product_tmpl_id=fields.Many2one('product.template','Formation')
    currency_id = fields.Many2one('res.currency')