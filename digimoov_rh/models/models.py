# -*- coding: utf-8 -*-

from odoo import models, fields, api


class digimoov_rh(models.Model):
    _inherit = ['hr.employee']

    test = fields.Char()
    cv = fields.Binary()
    grille = fields.Binary()
    contrat = fields.Binary()
    cnss = fields.Binary()
    rib = fields.Binary()
    cin = fields.Binary()
    fichepaie = fields.Binary()
    fichenote = fields.Binary()
    noteentretien = fields.Binary()
    attestationtravail = fields.Binary()
    attestationcongé = fields.Binary()
    autorisationexcepti = fields.Binary()

    embauchedate = fields.Date()
