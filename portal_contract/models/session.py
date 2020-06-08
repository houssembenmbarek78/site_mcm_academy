# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import time
from odoo.exceptions import ValidationError
import re


class Session(models.Model):
    _inherit = "mcm.session"

    name = fields.Char('Nom', required=True)
    action_type = fields.Many2one('mcm.action.formation', required=True)
    targeted_diploma = fields.Char('Diplôme visé', required=True)
    price_untaxed = fields.Monetary('Prix Unitaire HT', compute='_compute_price_untaxed', store=True, default=0.0)
    start_hour = fields.Char('De (Matin)')
    end_hour = fields.Char('À (Matin) ')
    start_second_hour = fields.Char('De (Aprés midi)')
    end_second_hour = fields.Char('À (Aprés midi) ')
    currency_id = fields.Many2one('res.currency')

    @api.depends('product_id')
    def _compute_price_untaxed(self):
        for rec in self:
            if (rec.product_id):
                if (rec.product_id.list_price and rec.product_id.duration):
                    rec.price_untaxed = rec.product_id.list_price / float(rec.product_id.duration)

    @api.onchange('start_hour','end_hour','start_second_hour','end_second_hour')
    def _check_session_time(self):
        time_re = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
        if self.start_hour:
            start_hour_format=bool(time_re.match(self.start_hour))
            if not start_hour_format:
                raise ValidationError(_("le format d'horaire rempli est faux,Veuillez respectez le format hh:mm"))

        if self.end_hour:
            end_hour_format=bool(time_re.match(self.end_hour))
            if not end_hour_format:
                raise ValidationError(_("le format d'horaire rempli est faux,Veuillez respectez le format hh:mm"))
        if self.start_second_hour:
            start_second_hour_format=bool(time_re.match(self.start_second_hour))
            if not start_second_hour_format:
                raise ValidationError(_("le format d'horaire rempli est faux,Veuillez respectez le format hh:mm"))
        if self.end_second_hour:
            end_second_hour_format=bool(time_re.match(self.end_second_hour))
            if not end_second_hour_format:
                raise ValidationError(_("le format d'horaire rempli est faux,Veuillez respectez le format hh:mm"))




