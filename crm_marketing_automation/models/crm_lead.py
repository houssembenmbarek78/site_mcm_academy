# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models,_
import calendar
from datetime import date,datetime


class CRM(models.Model):
    _inherit = "crm.lead"

    num_dossier=fields.Char(string="numéro de dossier")
    num_tel=fields.Char(string="numéro de téléphone")
    email=fields.Char(string="email")

