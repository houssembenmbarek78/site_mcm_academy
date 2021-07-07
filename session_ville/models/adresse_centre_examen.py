from odoo import api, fields, models, _


class Adresse_Centre_Examen(models.Model):
    _name = "session.adresse.examen"
    _rec_name = 'adresse_centre_examen'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Cette classe contient tous les informations nécessaire pour " \
                   "Les adresses des centres d'examens selon la ville choisi"

    adresse_centre_examen = fields.Char(required=True, help="Ajouter une adresse de centre d'examen")
    phone = fields.Char(string="N° téléphone de centre d'examen.",
                        help="Ajouter un numero de portable ou téléphone de centre d'examen.")
    email = fields.Char(help="Ajouter l'email de centre d'examen.")
    active = fields.Boolean('Active', default=True)
    session_ville_id = fields.Many2one('session.ville', help="Choisir une ville.")
    lien = fields.Char(default="https://", string="Lien d'accées au centre d'examen",
                       help="Lien de plan d'accès au centre d'examen sur Google Map")
