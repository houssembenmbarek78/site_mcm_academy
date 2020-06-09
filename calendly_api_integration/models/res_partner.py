# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class resPartner(models.Model):
    _inherit = "res.partner"

    formation_type=fields.Selection(selection=[
        ('taxi', 'TAXI'),
        ('vtc', 'VTC'),
    ], string='Formation')
    pole_emploi=fields.Char('ID POLE EMPLOI')
    social_security_number=fields.Char('Numéro securité social')
    funding_type=fields.Selection(selection=[
        ('cpf', 'CPF'),
        ('passformation', 'Pass formation '),
        ('perso', 'Perso'),
        ('pole_emploi', 'Pôle emploi(AIF)'),
    ], string='Type de financement')
    driver_licence=fields.Boolean('3 ans de permis ou plus')
    license_suspension=fields.Boolean('Aucun retrait définitif du permis ces 10 dernières années ')
    criminal_record=fields.Boolean('Casier judiciaire vierge B2')
    statut_calendly=fields.Selection(selection=[
        ('waiting', 'En attente de validation'),
        ('valid', 'Validé'),
    ], string='Statut client')

