# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Bank(models.Model):
    _inherit = "res.partner.bank"

    bank_code = fields.Char('Code banque',compute='_get_account_data_number' ,store=True,compute_sudo=True)
    guichet_code = fields.Char('Code guichet',compute='_get_account_data_number',compute_sudo=True)
    number_of_account = fields.Char('N° de compte',compute='_get_account_data_number',compute_sudo=True)
    rib = fields.Char('RIB',compute='_get_account_data_number',compute_sudo=True)
    bic = fields.Char('BIC')

    def _get_account_data_number(self):
        for rec in self:
            if rec.acc_number:
                if (len(rec.acc_number)==33):
                    bank_code=rec.acc_number[5:11]
                    bank_code=bank_code.replace(' ','')
                    rec.bank_code=bank_code
                    guichet_code=rec.acc_number[11:17]
                    guichet_code = guichet_code.replace(' ', '')
                    rec.guichet_code=guichet_code
                    number_of_account = rec.acc_number[17:31]
                    number_of_account = number_of_account.replace(' ', '')
                    rec.number_of_account = number_of_account
                    rib = rec.acc_number[31:]
                    rib = rib.replace(' ', '')
                    rec.rib = rib
