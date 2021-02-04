# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class resComapny(models.Model):
    _inherit = "res.partner"

    session_id = fields.Many2one('mcm.session','Session')
    partner_from = fields.Char('Partenaire')