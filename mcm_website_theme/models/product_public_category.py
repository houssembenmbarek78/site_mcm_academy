# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.public.category"

    code=fields.Char("Code")

    _sql_constraints = [
        ('code_uniq', 'unique (code)', "code déja existe pour une autre catégorie !"),
    ]