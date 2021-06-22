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



      for facture in factures:
         if (facture.company_id.id == 1) :
              if (facture.cpf_solde_invoice == True and facture.company_id.id ==1  or facture.cpf_acompte_invoice == True and facture.company_id.id ==1 or facture.invoice_user_id == 'ZOÉ' and facture.company_id.id ==1 ) :
                facture.methodes_payment = 'cpf'
                facture.pourcentage_acompte = 0
              elif facture.invoice_user_id != 'ZOÉ' and facture.company_id == 1:
                facture.methodes_payment = 'cartebleu'

