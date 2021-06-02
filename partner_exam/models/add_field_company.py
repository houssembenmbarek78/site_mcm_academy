from odoo import api, fields, models


class InheritResCompany(models.Model):
    _inherit = "res.company"
    _description = "Ajouter une signature dans l'interface de la société"

    signature_convocation = fields.Binary('Signature', store=True)
    region = fields.Char(default="Ile de France", string="Par le préfet de la région")

