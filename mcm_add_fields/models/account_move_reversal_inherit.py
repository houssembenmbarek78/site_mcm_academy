# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#Ce programme a été modifié par seifeddinne le 22/03/2021
#Modification du process de la facturation
#Modification de l'aperçu de la facturation
from odoo import models, fields, api
from odoo.tools.translate import _

class AccountMoveReversalInherit(models.TransientModel):
    _inherit = 'account.move.reversal'

    def _prepare_default_reversal(self, move):

        return {
            'ref': _('Reversal of: %s, %s') % (move.name, self.reason) if self.reason else _('Reversal of: %s') % (
                move.name),
            'date': self.date or move.date,
            'invoice_date': move.is_invoice(include_receipts=True) and (self.date or move.date) or False,
            'journal_id': self.journal_id and self.journal_id.id or move.journal_id.id,
            'invoice_payment_term_id': None,
            'auto_post': True if self.date > fields.Date.context_today(self) else False,
            'invoice_user_id': move.invoice_user_id.id,
            'pourcentage_acompte': move.pourcentage_acompte,
            'amount_residual' : move.amount_residual,

        }
