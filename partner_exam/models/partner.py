# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class resComapny(models.Model):
    _inherit = "res.partner"

    note_exam=fields.Char("Note d'examen blanc")
    note_exam_id = fields.One2many('info.examen', 'partner_id')
    note_exam_count = fields.Integer(compute="compute_notes_exams_count")
    this_is_technical_field = fields.Boolean(readonly=True, default=True)
    resultat = fields.Char(store=True, readonly=True, string="Résultat", compute="_get_default_value_resultat")
    info_exam_ids = fields.Many2one('info.examen', string='Resultat', store=True, readonly=True, compute="_get_default_value_resultat")
    
    @api.depends('note_exam_id', 'note_exam_id.resultat')
    def _get_default_value_resultat(self):
        """ Une fonction qui permet d'afficher 
                la resultat d'un client si (recu ou ajourné) du dernier ligne dans la list examens."""
        for rec in self:
            res = []
            rec.resultat = '__'
            if rec.note_exam_id:
                res = self.env['info.examen'].search([('partner_id', '=', rec.note_exam_id.partner_id.name)],
                                                         limit=1, order='create_date desc')
                self.info_exam_ids = res
                self.resultat = res.resultat
                return res

    def compute_notes_exams_count(self):
        for record in self:
            record.note_exam_count = self.env['info.examen'].search_count(
                [('partner_id', 'child_of', self.id)])

    def get_notes_history(self):
        self.ensure_one()
        return {
            "name": self.name,
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "info.examen",
            "type": "ir.actions.act_window",
            "domain": [("partner_id", "child_of", self.id)],
            'context': {'default_note_exam_id': self.note_exam_id.ids},
        }