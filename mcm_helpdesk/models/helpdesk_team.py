# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Helpdesk(models.Model):
    _inherit = "helpdesk.team"

    icon_class = fields.Char('Class icone')
    mcm_test = fields.Boolean('MCM Test')

class Ticket(models.Model):
    _inherit = "helpdesk.ticket"

    mcm_test = fields.Boolean('MCM Test')

