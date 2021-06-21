from odoo import fields, models


class InheritResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Inherit this class to add list of villes"

    session_ville_id = fields.Many2one('session.ville', string="Liste des villes")
