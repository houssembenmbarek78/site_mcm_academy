# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class resComapny(models.Model):
    _inherit = "res.partner"

    numero_cpf = fields.Char('Numéro CPF')
    statut_cpf = fields.Selection(selection=[
        ('untreated', 'Non Traité'),
        ('validated', 'Validé'),
        ('accepted', 'Accepté'),
        ('in_training', 'En Formation'),
        ('out_training', 'Sortie de Formation'),
        ('service_declared', 'Service Fait Declaré'),
        ('service_validated', 'Service Fait Validé'),
        ('bill', 'Facturé'),
        ('canceled', 'Annulé'),
    ], string='Statut CPF',default='untreated')
    date_cpf=fields.Datetime('Date CPF')