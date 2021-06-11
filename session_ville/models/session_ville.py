from odoo import api, fields, models, _


class SessionVille(models.Model):
    _name = "session.ville"
    _rec_name = 'name_ville'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Les villes"

    name_ville = fields.Char(string="Nom Ville")
    active = fields.Boolean('Active', default=True)
    description = fields.Text()
    session_adresse_examen_ids = fields.One2many('session.adresse.examen', 'session_ville_id')