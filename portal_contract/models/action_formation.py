# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Session(models.Model):
    _name = 'mcm.action.formation'
    _description = "action de formation"

    name=fields.Char('Nom')