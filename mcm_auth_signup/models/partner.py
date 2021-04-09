# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResPartner(models.Model):
    _inherit = "res.partner"

    firstname=fields.Char('Prénom')

    @api.model
    def signup_retrieve_info(self, token):
        res=super(ResPartner, self).signup_retrieve_info(token)
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        if partner.signup_valid:
            res['firstname'] = partner.firstname
            res['phone'] = partner.phone
        return res
