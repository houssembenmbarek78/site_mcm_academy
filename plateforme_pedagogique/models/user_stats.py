from odoo import models,fields,api

class User_stats(models.Model):
    _name = 'plateforme_pedagogique.user_stats'
    deleted =fields.Boolean(string='Supprimé')
    firstName = fields.Char(string='Nom')
    lastName = fields.Char(string='Prenom')
    mail =fields.Char(string='Email')
    user_id=fields.Many2one('res.partner')
    endTime=fields.Char(string="date de fin")
    totalTimeSpentInSeconds=fields.Char(string="Temps passé par seconde")
    progress=fields.Char(string='Progrès')
    score = fields.Char(string='Score')
    startTime = fields.Char(string='Date début')
    successfullyCompleted =fields.Boolean(string="complété avec succès")
    parcours_ids=fields.Many2one('plateforme_pedagogique.parcours')
