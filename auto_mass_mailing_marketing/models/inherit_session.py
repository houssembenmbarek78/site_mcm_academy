import datetime as datetime
from datetime import date, datetime, tzinfo, timedelta

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "mcmacademy.session"
    _description = "Add fields in session view"

    temps_convocation = fields.Selection(selection=[
        ('matin', 'Matin'),
        ('apres_midi', 'Après-Midi')],
        default="apres_midi", string="Examen Matin/Aprés Midi", help="Choisir un temp pour la session si Matin ou Apres Midi")

    heure_examen_matin = fields.Char(default="09H00")
    heure_examen_apres_midi = fields.Char(default="14H00")
    date_exam = fields.Date(string="Date d'examen")

    # Add adresse field pour l'afficher dans la convocation
    adresse_examen = fields.Char(required=True, string="Adresse D'examen", help="Ajouter l'adresse d'examen, "
                                                                                "cette information sera affiché dans les rapports PDF")
    date_convocation = fields.Date(string="Date d'envoi de convocation", default=datetime.today())
    horaire_email = fields.Char(compute="_compute_auto_horaire_email", string="Horaire Email",
                                help="Heure d'examen qui sera affiché "
                                     "dans le text de l'email pour la convocation.")

    def _compute_auto_horaire_email(self):
        """ This function for dynamic field in email template,
            used to display "time of exam", if field (temps_convocation == matin)
            the field horaire_email will display (09H00 Matin)
            else it will display (14H00 Aprés Midi) """
        if self.temps_convocation == 'matin':
            self.horaire_email = '09H00 Matin'
        elif self.temps_convocation == 'apres_midi':
            self.horaire_email = '14H00 Aprés Midi'
        else:
            self.horaire_email = " "

    def compute_count_prospect_ids(self):
        """ Number of clients with state (Indécis) """
        for record in self:
            record.prospect_count = self.env['res.partner'].search_count(
                [('id', 'in', [x.id for x in self.prospect_ids])])

    #Add this compute field to call the function calculate the number
    prospect_count = fields.Integer(compute='compute_count_prospect_ids')

    def compute_count_client_ids(self):
        for record in self:
            record.clients_count = self.env['res.partner'].search_count(
                [('id', 'in', [a.id for a in self.client_ids])])

    clients_count = fields.Integer(compute='compute_count_client_ids')

    def get_list_of_partner_indecis(self):
        """ this function for smart button in session
        view to display all client with state = Indécis """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Client Indécis',
            'view_mode': 'tree',
            'res_model': 'res.partner',
            'domain': [('id', 'in', [x.id for x in self.prospect_ids])],
            'context': "{'create': True}"
        }

    def get_list_of_partner_gagne(self):
        """ this function for smart button in session
        view to display all client with state = Indécis """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Client Gagné',
            'view_mode': 'tree, form',
            'res_model': 'res.partner',
            'domain': [('id', 'in', [x.id for x in self.client_ids])],
            'context': "{'create': True}"
        }
