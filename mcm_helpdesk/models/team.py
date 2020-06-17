# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.team'

    icon_css = fields.Char('Icone',store=True,default='fa fa-home')