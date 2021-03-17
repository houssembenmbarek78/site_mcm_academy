import functools
import xmlrpc.client
import requests
from requests.structures import CaseInsensitiveDict

from odoo import models, fields


class partner(models.Model):
    _inherit = 'res.partner'

    # ajouter champs au modele partner par defaut res.partner ne sont pas des instructors
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('test.session', string='attended_sessions',

                                   readonly=True)
    #champs pour recuperer les statistiques

    last_login=fields.Char(string="derniere Connexion")
    # learner_achivement=fields.Char(string="Réalisations des apprenants")
    averageScore=fields.Char(string="Score Moyenne")
    totalTimeSpentInMinutes=fields.Char(string="temps passé en minutes")
  # methode pour recuperer les utilisateurs de 360learning
    def getusers(self):

        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        response = requests.get('https://app.360learning.com/api/v1/users', params=params)
        users = response.json()
        #faire un parcours sur chaque user et extraie ses statistique
        for user in users:
            iduser=user['_id']
            response_user=requests.get('https://app.360learning.com/api/v1/users'+ iduser ,params=params)
            table_user=response_user.json()
           # Affecter les infos recupérés aux champs du res.partner
            values={
                "last_login": table_user['lastLoginAt'],
                "averageScore": table_user['averageScore'],
                "totalTimeSpentInMinutes": table_user['totalTimeSpentInMinutes']
            }

            self.env['res.partner'].sudo().create(values)
        print("users-----", values)
        # res = requests.get('https://app.360learning.com/api/v1/programs/sessions', params=params)
        # program_sessions = res.json()
        # # for record in program_sessions:
        # #  print('programsessions',record)
        #
        #
        # # for r in users:
        # #  id = r['_id']
        #
        # re=requests.get('https://app.360learning.com/api/v1/programs/sessions/5f96eda86fdf5a4ae5ee05ea/stats',params=params)
        # pogramstat=re.json()
        # print("program name", pogramstat['name'])
        # userstat=pogramstat['usersStats']
        # for r in userstat:
        #  print('prog stat',r)







    def post(self):
      company_id = '56f5520e11d423f46884d593'
      api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
      url = "https://app.360learning.com/api/v1/users?company=" + company_id + "&apiKey=" + api_key

      headers = CaseInsensitiveDict()
      headers["Content-Type"] = "application/json"

      data = '{"mail":"cegem27231@heroulo.com"}'

      resp = requests.post(url, headers=headers, data=data)

      print(resp.status_code)


    def delete(self):
     company_id = '56f5520e11d423f46884d593'
     api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
     headers = CaseInsensitiveDict()
     headers["Accept"] = "*/*"
     email = "lahmerines7@gmail.com"
     url = "https://app.360learning.com/api/v1/users/lahmerines7@gmail.com?company=" + company_id + "&apiKey=" + api_key
     resp = requests.delete(url)

     print(resp.status_code)
