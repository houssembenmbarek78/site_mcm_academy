# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools import datetime, base64
from odoo.exceptions import ValidationError


class NoteExamen(models.Model):
    _name = "info.examen"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Les Notes et les informations des examens"

    partner_id = fields.Many2one('res.partner', string="Client")
    epreuve_a = fields.Float(string="Epreuve A(QCM):", track_visibility='always')
    epreuve_b = fields.Float(string="Epreuve B(QRO)", track_visibility='always', default=1)
    moyenne_generale = fields.Float(string="Moyenne Générale", track_visibility='always', store=True)
    mention = fields.Selection(selection=[
        ('recu', 'reçu'),
        ('ajourne', 'ajourné')],
        string="Mention", default=False)
    resultat = fields.Selection(selection=[
        ('recu', 'Reçu'),
        ('ajourne', 'Ajourné')], string="Résultat")
    date_exam = fields.Date(string="Date Examen",  track_visibility='always')
    active = fields.Boolean('Active', default=True)
    module_ids = fields.One2many('mcmacademy.module', 'info_examen_id')
    date_today = fields.Date(string="Date d'envoi de relevée de note: ", default=datetime.today())
    company_id = fields.Many2one(
        'res.company', string='Company', change_default=True,
        default=lambda self: self.env.company,
        required=False, readonly=False)
    nombre_de_passage = fields.Selection(selection=[
        ('premier', 'premier'),
        ('deuxieme', 'deuxième'),
        ('troisieme', 'troisième')],
        string="Nombre De Passage", default="premier")

    presence = fields.Selection(selection=[
        ('present', 'Présent'),
        ('Absent', 'Absent')],
        string="Présence", default='present')
    # Ajout le champ etat qui sera invisible dans l'interface "notes & examen"
    # Utilisation de ce champ pour une information dans le fichier xml de "attestation de suivi de formation
    etat = fields.Char(compute="etat_de_client_apres_examen")

    @api.onchange('epreuve_a', 'epreuve_b', 'presence')
    def _compute_moyenne_generale(self):
        """ This function used to auto display some result
        like the "Moyenne Generale" & "Mention" & "Resultat" """
        for rec in self:
            rec.moyenne_generale = (rec.epreuve_a + rec.epreuve_b) / 2
            if rec.epreuve_a >= 10 and rec.epreuve_b >= 8 and rec.moyenne_generale >= 12:
                rec.moyenne_generale = rec.moyenne_generale
                rec.mention = 'recu'
                rec.resultat = 'recu'
                rec.presence = 'present'
            else:
                # reset your fields
                rec.epreuve_a = rec.epreuve_a
                rec.epreuve_b = rec.epreuve_b
                rec.mention = 'ajourne'
                rec.resultat = 'ajourne'
                if rec.epreuve_a >= 1 and rec.epreuve_a < 21:
                    rec.presence = 'present'
                elif rec.epreuve_a < 1 and rec.epreuve_b < 1:
                    rec.presence = 'Absent'
                if rec.epreuve_b >= 1 and rec.epreuve_b < 21:
                    rec.presence = 'present'
                elif rec.epreuve_a < 1 and rec.epreuve_b < 1:
                    rec.presence = 'Absent'

    def write_compute_moyenne_generale(self, epreuve_a, epreuve_b):
        """ This function used in write methode to update fields
        when user import new notes """
        self.moyenne_generale = (epreuve_a + epreuve_b) / 2
        if epreuve_a >= 10 and epreuve_b >= 8 and self.moyenne_generale >= 12:
            moyenne_generale = self.moyenne_generale
            self.mention = 'recu'
            self.resultat = 'recu'
            self.presence = 'present'
        else:
            # reset your fields
            self.mention = 'ajourne'
            self.resultat = 'ajourne'
            if epreuve_a >= 1 and epreuve_a < 21:
                self.presence = 'present'
            elif epreuve_a < 1 and epreuve_b < 1:
                self.presence = 'Absent'
            if epreuve_b >= 1 and epreuve_b < 21:
                self.presence = 'present'
            elif epreuve_a < 1 and epreuve_b < 1:
                self.presence = 'Absent'

    @api.onchange("résultat")
    def etat_de_client_apres_examen(self):
        """Fonction pour mettre le champs etat
        automatique depend de champ resultat,
        pour l'utilisé dans la template de "Atestation de suivi de formation" """
        for rec in self:
            if rec.resultat == 'recu':
                rec.etat = "avec succès"
            if not rec.resultat == "recu":
                rec.etat = "sans succès"
    
    def remove_double_line_with_same_date(self):
        duplicate_exams = []
        for partner in self:
            if partner.date_exam and partner.id not in duplicate_exams:
                duplicates = self.env['info.examen'].search([('partner_id', '=', partner.partner_id.id), ('id', '!=', partner.id), ('date_exam', '=', partner.date_exam)])
                print(duplicates)
                for dup in duplicates:
                    print("dup", dup)
                    duplicate_exams.append(dup.id)
                    print("duplicate_contacts", duplicate_exams)
        self.browse(duplicate_exams).unlink()
        
    @api.model
    def create(self, vals_list):
        res = super(NoteExamen, self).create(vals_list)
        print(vals_list)
        res._compute_moyenne_generale()
        return res

    def write(self, vals):
        """ Lors de modification d'un nouveau enregistrement des notes d'examen,
                cette fonction permet de verifier si il y'a un autre enregistrement
                contient meme date d'examen, l'ancienne ligne sera
                supprimer et remplacer par la nouvelle ligne avec les champs dynamique"""
        if 'epreuve_a' in vals and not 'epreuve_b' in vals:
            self.write_compute_moyenne_generale(vals['epreuve_a'], self.epreuve_b)
        elif 'epreuve_a' in vals and 'epreuve_b' in vals:
            self.write_compute_moyenne_generale(vals['epreuve_a'], vals['epreuve_b'])
        elif 'epreuve_b' in vals and not 'epreuve_a' in vals:
            self.write_compute_moyenne_generale(self.epreuve_a, vals['epreuve_b'])
        return super(NoteExamen, self).write(vals)


