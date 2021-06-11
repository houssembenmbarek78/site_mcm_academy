# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ModuleDetails(models.Model):
    _name = 'mcmacademy.module.details'
    _description = "Details de modules"

    name = fields.Char('Nom', required=True)
    prix_normal=fields.Monetary('Prix Particulier')
    prix_chpf=fields.Monetary('Prix CHPF')
    duree = fields.Char('Durée')
    module_id=fields.Many2one('mcmacademy.module','Module')
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)