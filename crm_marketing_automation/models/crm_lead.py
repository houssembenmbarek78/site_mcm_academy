# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
from odoo import api, fields, models,_
import calendar
from datetime import date,datetime


class CRM(models.Model):
    _inherit = "crm.lead"

    num_dossier=fields.Char(string="numéro de dossier",)
    num_tel=fields.Char(string="numéro de téléphone")
    email=fields.Char(string="email")
    mode_de_financement = fields.Selection(selection=[
        ('particulier', 'Personnel'),
        ('cpf', 'Mon Compte Formation, CPF'),
        ('chpf', 'Région Hauts-de-France, CHPF'),
        ('aif', 'Pôle emploi, AIF'),
    ], string='Mode de financement', default="particulier")
