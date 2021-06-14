from odoo import api, fields, models


class McmacademySessionVille(models.Model):
    _inherit = "mcmacademy.session"
    _description = "Inherit this mcmacademy.session to add list of villes"

    session_ville_id = fields.Many2one('session.ville')
    session_adresse_examen =fields.Many2one('session.adresse.examen')
    phone = fields.Char(related="session_adresse_examen.phone")
    email = fields.Char(related="session_adresse_examen.email")
    # Add new field "lien" contains link of center adress exam
    lien = fields.Char(related="session_adresse_examen.lien", string="Lien d'accées au centre d'examen")
    @api.onchange('session_ville_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'session_adresse_examen': [('session_ville_id', '=', rec.session_ville_id.id)]}}