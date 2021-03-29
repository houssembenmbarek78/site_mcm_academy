from odoo import fields,models,api,exceptions
import requests
class Parcours(models.Model):
    _name = 'test.parcours'

    id_parcours=fields.Char(string="id Parcours")
    hasUserLimit=fields.Boolean(string="limite")
    endDate= fields.Char(string="Date Début")
    programTemplate =fields.Char(string="id programTemplate")
    startDate=fields.Char(string="Date fin")
    groupe_id=fields.Many2one('test.groupe',string='groupe')
    name = fields.Char(string="Nom")
    programDuration=fields.Integer(string="Durée du programme")
    programDurationType=fields.Char(string="Type de Programme")

    def getParcours(self):
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        # resgroupe=requests.get('https://app.360learning.com/api/v1/groups',params=params)
        # for groupe in resgroupe.json():
        #     id_groupe=groupe['_id']
        #     print('groupe',groupe)
        resparcours = requests.get('https://app.360learning.com/api/v1/groups/56f5520e11d423f46884d594/programs',params=params)
        for parcours in resparcours.json():
            print('parcours***************',len(resparcours.json()),parcours)