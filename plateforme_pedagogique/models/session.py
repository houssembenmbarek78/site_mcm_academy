from odoo import _
from odoo import models, fields,api
from datetime import datetime,timedelta,date
from odoo.exceptions import ValidationError
import functools
import xmlrpc.client
import requests
from requests.structures import CaseInsensitiveDict

class Session(models.Model):
    _inherit='mcmacademy.session'

    #Supprimer session  automatiquement  de plateforme 360
    # après 4jours de date d'examen
    def supprimer_session_automatque(self):
        company_id = '56f5520e11d423f46884d593'
        api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "*/*"
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        url_groups = 'https://app.360learning.com/api/v1/groups'
        response_grps = requests.get(url_groups, params=params)
        groupes = response_grps.json()
        print(response_grps.json())
        #Trouver la session de 360 sur odoo
        #Récuperer la date d'examen, calculer la date de suppression(+4jours)
        # puis supprimer le groupe
        for groupe in groupes:
            nomgroupe = str(groupe['name']).lower()
            id_groupe = groupe['_id']
            find_session=self.env['mcmacademy.session'].sudo().search([('name',"=",nomgroupe)])
            if find_session:
                if find_session.date_exam:
                    ville = str(find_session.ville).lower()
                    date_exam = str(find_session.date_exam).lower()
                    print('date d\'examen', find_session.date_exam)
                    # date de suppression est date d'examen + 4jours
                    date_suppression = find_session.date_exam + timedelta(days=4)
                    today = date.today()
                    if ((date_suppression <= today) and (ville in nomgroupe) and (date_exam in nomgroupe)):
                        print('date_sup', find_session.date_exam, date_suppression, today)
                        # url = 'https://app.360learning.com/api/v1/groups/'+id_groupe+'?company=' + company_id + '&apiKey=' + api_key
                        # resp = requests.delete(url)
                        print('url', 'resp.status_code')
                    else:
                      print('date incompatible', find_session.name)

    # Supprimer session manuellement de plateforme 360
    def supprimer_session_manuelle (self):
        company_id = '56f5520e11d423f46884d593'
        api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "*/*"
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        url_groups = 'https://app.360learning.com/api/v1/groups'
        response_grps = requests.get(url_groups, params=params)
        existe = False
        groupes = response_grps.json()
        print(response_grps.json())
        # Trouver la session de 360 sur odoo
        # puis supprimer le groupe
        for groupe in groupes:
            nomgroupe = str(groupe['name']).lower()
            id_groupe = groupe['_id']
            ville =str(self.ville).lower()
            date_exam=str(self.date_exam).lower()
            if  ((ville in nomgroupe) and (date_exam in nomgroupe) ):
                        print('date_sup', )
        #                 url = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '?company=' + company_id + '&apiKey=' + api_key
        #                 resp = requests.delete(url)
                        print('url', 'resp.status_code')
