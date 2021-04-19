# -*- coding: utf-8 -*-

from odoo import models, fields, api


class jours_feries(models.Model):
    _name = 'jours_feries.jours_feries'
    _description = 'jours_feries.jours_feries'

    name = fields.Char()
    jours = fields.Integer()
    date_debut = fields.Date()
    date_fin = fields.Date()
    pays = fields.Selection([('tunisie', 'Tunisie'), ('france', 'France')])
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
