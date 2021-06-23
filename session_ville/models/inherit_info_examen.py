from odoo import api, fields, models


class InheritInfoExamen(models.Model):
    _inherit = "info.examen"
    _description = "Inherit this infi.examen to add list of villes"

    ville_id = fields.Many2one('session.ville')
