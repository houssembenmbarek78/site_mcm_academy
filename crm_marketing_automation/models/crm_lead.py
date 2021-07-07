# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models,_
import calendar
from datetime import date,datetime


class CRM(models.Model):
    _inherit = "crm.lead"

    num_dossier=fields.Char(string="numéro de dossier",related='partner_id.numero_cpf')
    num_tel=fields.Char(string="numéro de téléphone",related='partner_id.phone')
    email=fields.Char(string="email",related='partner_id.email')
    mode_financement=fields.Char(string="mode_financement",related='partner_id.mode_de_financement')
