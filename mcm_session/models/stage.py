# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Module(models.Model):
    _name = 'mcmacademy.stage'

    name=fields.Char("Nom d'état")