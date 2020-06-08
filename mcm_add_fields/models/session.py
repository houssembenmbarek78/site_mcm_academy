# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Session(models.Model):
    _name = 'mcm.session'

    product_id=fields.Many2one('product.template',string="Formation",required=True)
    start_date=fields.Date(required=True)
    end_date=fields.Date(required=True)
    state=fields.Many2one('res.country.state',string="Département",required=True)
    partner_ids=fields.One2many('res.partner','session_id','Partners')