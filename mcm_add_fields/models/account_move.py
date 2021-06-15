# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#Ce programme a été modifié par seifeddinne le 22/03/2021
#Modification du process de la facturation
#Modification de l'aperçu de la facturation
from odoo import api, fields, models,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from  _datetime import datetime,date


class AccountMove(models.Model):
    _inherit = "account.move"
#Déclaration des fields
#On a ajouté ces champs :
    #restamount / acompte_invoice /pourcentage_acompte
    mcm_paid_amount = fields.Monetary(string='Montant payé',compute='_get_mcm_paid_amount',store=True)
    acompte_invoice = fields.Boolean(default=False)
    cpf_solde_invoice = fields.Boolean(default=False)
    cpf_acompte_invoice = fields.Boolean(default=False)
    cpf_solde_invoice =fields.Boolean(default=False)
    amount_residual = fields.Monetary(string='Montant due',compute='_get_mcm_paid_amount',store=True)
    amount = fields.Monetary(string='Montant',compute='_compute_payments_widget_to_reconcile_info',store=True)
    amount_paye = fields.Monetary(string='Montant payé',store=True,readonly=True,compute='_compute_change_amount')
    restamount = fields.Monetary(string='Reste à payé ',compute='_compute_change_amount',store=True,readonly=True)
    module_id = fields.Many2one('mcmacademy.module','Module')
    session_id = fields.Many2one('mcmacademy.session','Session')
    pricelist_id = fields.Many2one('product.pricelist','Liste de prix')
    methodes_payment = fields.Selection(selection=[('cpf','CPF'),('cartebleu','Cartebleu')],String='Méthode de payment')
    cpf_acompte_amount = fields.Monetary('Montant acompte')
    pourcentage_acompte = fields.Integer(string="Pourcentage d'acompte",compute='_compute_change_amount',store=True,readonly=False)



    @api.depends('amount_total', 'amount_residual')
    def _get_mcm_paid_amount(self):
        for rec in self:
            payments = self.env['account.payment'].search(['|','&',('communication', "=", rec.name),('state', "=", 'posted'),('communication', 'like', rec.invoice_origin)])
            paid_amount = 0.0
            for payment in payments:
                paid_amount += payment.amount
            rec.mcm_paid_amount = paid_amount
#Fonction qui calcule le reste à payé ,le montant de la formation et le pourcentage de l'acompte lhors de la modification de l'acompte
#On traite les cas celon deux critere en_interne ou par site web
    #On calcule le montant total untaxed , le montant_paye , le restamount
    # le montant residual doit avoir le rest du montant
    #amount_residual_signed c'est pour l'avoir il prend le reste a paye
    #amount_total_signed c est aussi por l'avoir il prend le reste à payer
    #on a deux condition par site web ou en interne :
    #Si la méthode de payment est cpf et le champs   methode_payment == CPF alors :
    # la vue de la facture change elle affiche l'acompte qui prend sa valeur default 25 %
    # et on peux la changer en pourcentage qu' on veux tout en calculant le montant payée et le reste à payer correctement
    #Si non si la méthode de payment est par carte bleu et le champs methode_payment== 'cartebleu' : l'acompte ne  s'affiche pas et la facture prend la somme de la formation
#
    @api.depends('invoice_line_ids.price_subtotal','pourcentage_acompte','methodes_payment','company_id')
    def _compute_change_amount(self):
         date_precis = date(2021, 6, 10)

         for rec in self:
            amount_untaxed_initiale = rec.amount_untaxed
            invoice_date=rec.invoice_date
            daysDiff = 0
            if  date_precis and rec.invoice_date:
                 daysDiff = ((date_precis) - rec.invoice_date).days
                 if (rec.methodes_payment == 'cpf' and daysDiff > 0 ):
                    rec.pourcentage_acompte = 0
                    rec.amount_paye = (rec.amount_untaxed * rec.pourcentage_acompte) / 100
                    rec.restamount = amount_untaxed_initiale - rec.amount_paye
                    # rec.amount_untaxed =  rec.amount_paye
                    # rec.amount_residual = rec.restamount
                
                    rec.amount_residual_signed = rec.restamount
                    rec.amount_total_signed = rec.restamount
                 elif (rec.methodes_payment == 'cpf' and daysDiff <= 0  and rec.company_id.id == 2 ):
                    rec.pourcentage_acompte = 25
                    rec.amount_paye = (rec.amount_untaxed * rec.pourcentage_acompte) / 100
                    rec.restamount = amount_untaxed_initiale - rec.amount_paye
                    # rec.amount_untaxed =  rec.amount_paye
                    # rec.amount_residual = rec.restamount
                    rec.amount_residual_signed = rec.restamount
                    rec.amount_total_signed = rec.restamount





                # elif (rec.methode_payment == 'cartebleu'):
                #     # rec.pourcentage_acompte = 0
                #     # amount_untaxed = rec.invoice_line_ids.price_subtotal
                #     print("testmontant web")
                #     print(rec.invoice_line_ids.price_subtotal)
                #     print(rec.amount_untaxed)

    # @api.model
    # def write (self, vals):
    #     residual_amounts_list = super(AccountMove, self).create(vals)
    #     for rec in self :
    #     #     rec.amount_residual = rec.restamount
    #         print("hhhh")
    #     return residual_amounts_list

#Annulation de l'acompte
    def delete_invoice(self):
        moves=self.env['account.payment'].search([])
        for move in moves:
            move.name='/'
            move.line_ids.unlink()
            move.sudo().unlink()

