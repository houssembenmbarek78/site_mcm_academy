# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "helpdesk.team"

    icon_class = fields.Char('Class icone',default='fa fa-home')

