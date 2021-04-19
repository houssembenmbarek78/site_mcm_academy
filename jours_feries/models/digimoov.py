from odoo import models, fields, api


class digimoov(models.Model):
    _name = 'jours_feries.digimoov'
    _description = 'jours_feries.digimoov'

    name = fields.Char(required=True)
    description = fields.Char()
    date_debut = fields.Date(required=True)
    date_fin = fields.Date(required=True)
    pays = fields.Selection([('tunisie', 'Tunisie'), ('france', 'France')])
    remuneration = fields.Selection([('oui', 'Oui'), ('non', 'Non')], required=True)

    _sql_constraints = [
        ('date_check2', "CHECK ((date_debut <= date_fin))", "The start date must be anterior to the end date."),

    ]