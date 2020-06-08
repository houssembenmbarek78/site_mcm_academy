# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class resPartner(models.Model):
    _inherit = "res.partner"

    special_tarif = fields.Boolean('Tarif spéciale', store=True)
    discount_name = fields.Char(' ')
    discount = fields.Monetary(' ', store=True)
    signature_partner = fields.Binary('Signature', store=True)

