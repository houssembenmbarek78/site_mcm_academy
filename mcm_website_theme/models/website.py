# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.http import request

class Website(models.Model):
    _inherit = "website"

    @api.model
    def get_states(self):
        state_ids = self.env['res.country.state'].sudo().search([('country_id.code', 'ilike', 'FR')])
        return state_ids

    def get_user_name_logged(self):
        return request.env.user.name

    def get_user_email_logged(self):
        return request.env.user.email


