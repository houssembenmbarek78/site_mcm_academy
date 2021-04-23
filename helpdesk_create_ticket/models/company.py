# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,tools

class HelpdeskTicket(models.Model):
    _inherit = "res.company"

    alias_domain = fields.Char('Domaine Alias')