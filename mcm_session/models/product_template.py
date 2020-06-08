# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class product_template(models.Model):
    _inherit = "product.template"

    prix_chpf = fields.Float(
        'Prix CHPF', default=1.0,
        digits='Product Price',
        help="Prix CHPF")
