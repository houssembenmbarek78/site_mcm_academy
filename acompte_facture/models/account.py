#Ce programme a été modifié par seifeddinne le 22/03/2021
#Modification du process de la facturation
#Modification de la facture_client

from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit = "account.move"
    restamount = fields.Monetary(string='Reste à payé ', store=True)
    amount_paye= fields.Monetary(string='payé ', store=True)
#Ancien _Process  :
# #Création de l'acompte dans l'ancien process
#
#     def action_create_acompte(self):
#         for rec in self:
#             print('montant total')
#             print(self.amount_total)
#             return {
#                 'name':"Créer une facture d'acompte",
#                 'type': 'ir.actions.act_window',
#                 'view_mode': 'form',
#                 'res_model': 'account.invoice.acompte.wizard',
#                 'target': 'new',
#                 'context': {
#                     'default_invoice_id': self.ids[0],
#                     'default_pourcentage': 100,
#                 },
#             }

    # Fonction qui calcule le reste à payé ,le montant de la formation avec  pourcentage d'acompte dans la facture
    # Calculer les montants: restamount , amount_residual , amount_paye l'hors du chagement du pourcentage d'acompte
    # Valeurs changer l'hors de  la modification du pourcentage et en calculant le montant payé et le reste à payer
    # On sépare le process de facturation par le champs principal methode_payment qui peux etre sois cpf sois carte_bleu
    #on n oublie pas qu'on travaille avec la multi_compagnie:
    # company_id.id== 1  MCM_Academy
    #company_id.id== 2   Digimoov
    @api.onchange('pourcentage_acompte')
    def _compute_amount(self):
        invoice=super(AccountMove,self)._compute_amount()
        for rec in self:
            if (rec.methodes_payment == 'cpf' and rec.company_id.id== 2) :
                amount_untaxed_initiale = rec.amount_untaxed
                rec.amount_paye=(rec.amount_untaxed*rec.pourcentage_acompte)/100
                # rec.amount_untaxed = (rec.amount_untaxed * rec.pourcentage_acompte) / 100
                rec.restamount = amount_untaxed_initiale - rec.amount_paye
                # rec.amount_residual = rec.restamount
                # rec.amount_residual= rec.amount_untaxed
                amount_residual_signed = rec.restamount
                return invoice
            elif (rec.methodes_payment == 'cartebleu') :

                rec.amount_untaxed = rec.amount_total
class resPartnerWizard(models.TransientModel):
    _name = 'account.invoice.acompte.wizard'
    _description = 'wizard to change total amount and invoice line (acompte invoice)'
    invoice_id=fields.Many2one('account.move','Facture')
    amount=fields.Monetary("Montant d'Acompte",default=lambda self:self.invoice_id.amount_total)
    pourcentage = fields.Integer("Pourcentage d'Acompte")
    restamount= fields.Monetary("Rest Montant",default=lambda self:self.invoice_id.amount_total-(self.invoice_id.amount_total*self.pourcentage)/100)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    def action_create_acompte(self):
        self.invoice_id.button_draft()
        lines = self.invoice_id.line_ids.sorted('debit')
        self.invoice_id.write({
            'amount_total':self.amount,
            'pourcentage_acompte':self.pourcentage,
            'acompte_invoice':True,
        })
        # for line in self.invoice_id.invoice_line_ids:
        #     balance=line.debit-self.amount
        #     debit=0.0
        #     credit=self.amount
        #     price_unit=self.amount
        #     line.write({
        #     'price_unit': price_unit,
        #     'debit': debit,
        #     'credit': credit,
        #     'balance': balance,
        #     })
        self.invoice_id.post()

    @api.onchange('pourcentage')
    def change_amount(self):
        for rec in self:
            rec.amount=(rec.amount*rec.pourcentage)/100






