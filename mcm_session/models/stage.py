# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Module(models.Model):
    _name = 'mcmacademy.stage'
    _description = "Etats des sessions"

    name=fields.Char("Nom d'état")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)