# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    state_ids = fields.Many2many('res.country.state','product_template_state_rel', 'product_template_id', 'state_id', string='States')



