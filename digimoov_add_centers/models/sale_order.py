# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api

class Sale(models.Model):
    _inherit = "sale.order"

    # ajouter des nouveaux centres d'examens à l'aide de l'option selection_add
    ville = fields.Selection(selection_add=[('nice', 'Nice'),('montpellier', 'Montpellier'),('rouen', 'Rouen'),('grenoble', 'Grenoble'),('rennes', 'Rennes'),('metz', 'Metz'),('bourges', 'Bourges')])