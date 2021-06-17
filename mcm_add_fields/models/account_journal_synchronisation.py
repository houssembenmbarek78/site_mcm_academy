# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#Ce programme a été modifié par seifeddinne le 22/03/2021
#Modification du process de la facturation
#Modification de l'aperçu de la facturation
from odoo import api, fields, models,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from datetime import datetime , date

class AccountJournalSynchronisation(models.Model):
    _inherit = "account.journal"

    # Synchroniser les factures recentes
    def synchronisation_recent_invoice(self):
      factures = self.env['account.move'].search([])
      My_date = date(2021, 4, 28)
      daysDiff = 0

      for facture in factures:
        if (facture.invoice_date and My_date) :
          daysDiff = ((My_date) - facture.invoice_date).days
          if daysDiff == 1 :
             if (facture.cpf_solde_invoice == True  or facture.cpf_acompte_invoice == True or facture.invoice_user_id == 'ZOÉ' ) :
                facture.methodes_payment = 'cpf'
                facture.pourcentage_acompte = 0
             elif facture.invoice_user_id != 'ZOÉ' :
                facture.methodes_payment = 'cartebleu'
          elif daysDiff == 0 :
              if (facture.cpf_solde_invoice == True or facture.cpf_acompte_invoice == True or facture.invoice_user_id == 'ZOÉ'):
                  facture.methodes_payment = 'cpf'
              elif facture.invoice_user_id != 'ZOÉ':
                  facture.methodes_payment = 'cartebleu'



