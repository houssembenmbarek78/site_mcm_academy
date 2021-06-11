# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Domaine(models.Model):
    _name = 'mcmacademy.domain'
    _description = "Domaine de formation"

    name=fields.Char("Nom de domaine de formation")
    code=fields.Integer("Code")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)