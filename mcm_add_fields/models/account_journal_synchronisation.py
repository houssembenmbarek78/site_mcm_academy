# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#Ce programme a été modifié par seifeddinne le 22/03/2021
#Modification du process de la facturation
#Modification de l'aperçu de la facturation
from odoo import api, fields, models,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from datetime import datetime
from datetime import date, datetime
import datetime






class AccountJournalSynchronisation(models.Model):
    _inherit = "account.journal"

    # Synchroniser les factures recentes
    def synchronisation_recent_invoice(self):
        factures = self.env['account.move'].search([])
        # currentDate = datetime.datetime.strptime('09062021', '%d%m%Y').date()
        My_date = datetime.datetime.strptime('08062021', '%d%m%Y').date()


        for facture in factures:
            if ((facture.cpf_solde_invoice == True and (facture.invoice_date) < My_date) or (facture.cpf_acompte_invoice == True and  facture.invoice_date < My_date) or (facture.invoice_user_id == 'ZOÉ' and facture.invoice_date < My_date)):
                facture.methodes_payment = 'cpf'
            elif (facture.invoice_user_id != 'ZOÉ'):
                facture.methodes_payment = 'cartebleu'

