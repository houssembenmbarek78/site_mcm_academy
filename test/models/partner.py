import functools
import xmlrpc.client
import requests
from requests.structures import CaseInsensitiveDict

from odoo import models, fields,api
from datetime import datetime

class partner(models.Model):
    _inherit = 'res.partner'
    #apprenant = fields.Boolean("Apprenant", default=True)
    # Ajouter champs au modele partner par defaut res.partner ne sont pas des instructors
    apprenant=fields.Boolean()
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('test.session', string='attended_sessions',
                                   readonly=True)
    assignedPrograms = fields.Integer(string='Nombre de programmes attribués')
    # certification_ids = fields.One2many('test.certification', string='certifications')
    toDeactivateAt = fields.Date(string='date de suppression', default='')
    # groupe_admin_ids= fields.Many2many('test.groupe', string='groupes à gérer')
    # groupe_user_ids =fields.Many2many('test.groupe', string='groupes à suivre')

    #Champs pour recuperer les statistiques
    last_login=fields.Char(string="derniere Connexion")
    # learner_achivement=fields.Char(string="Réalisations des apprenants")
    averageScore=fields.Char(string="Score Moyen")
    totalTimeSpentInMinutes=fields.Char(string="temps passé")
    #Champs pour stocker le mot de passe
    password360=fields.Char()
    firstName = fields.Char()
    lastName = fields.Char()
    statut_client = fields.Char(string="Statut Client")
    validation= fields.Boolean(string="Validé")
    # Creer une fiche client pour faire un test
    def createuser(self):
        partner = self.env['res.partner'].sudo().create({
            'name': 'youcef',
            'email': 'youcefallahoum@gmail.com'})
        print('created,', partner)

    def createtest(self):
        partner = self.env['res.partner'].sudo().create({
            'name': 'test',
            'email': 'kadilo3413@gameqo.com'})
        print('created,', partner)


    #Recuperer les utilisateurs de 360learning
    def getusers(self):

        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        response = requests.get('https://app.360learning.com/api/v1/users', params=params)
        users = response.json()
        #Faire un parcours sur chaque user et extraire ses statistiques
        for user in users:
            iduser=user['_id']
            email=user['mail']
            response_user=requests.get('https://app.360learning.com/api/v1/users/'+iduser ,params=params)
            table_user=response_user.json()
            #print(table_user)
            lastlogin = str(table_user['lastLoginAt'])
            average = str(table_user['averageScore']) if table_user['averageScore'] else ''
            if (len(lastlogin) > 0 ):
                date_split = lastlogin[0:19]
                date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                new_format = '%d %B, %Y'
                last_login = date.strftime(new_format)
                print(last_login)
            #Chercher par email le meme client pour lui affecter les stats de 360
                partners= self.env['res.partner'].sudo().search([('email', "=",email)])
                for partner in partners:
                    if partners:

                            partner.sudo().write({
                            'last_login': last_login,
                            'averageScore':average,
                            'totalTimeSpentInMinutes': table_user['totalTimeSpentInMinutes'],
                            'assignedPrograms': table_user['assignedPrograms'],
                            'toDeactivateAt': table_user['toDeactivateAt'],
                            'apprenant':True,
                             })
                            print("partner",partner.last_login)




    #Ajouter i-One sur 360
    @api.constrains('statut_client','validation')
    def post(self):
        if (self.statut_client == 'Gagné' and self.validation):
            espace = self.name.find('')

            if espace:
                name = self.name.split()
                self.firstName = name[0]
                self.lastName = name[1:len(name)]
                print(self.firstName, self.lastName)
            else:
                if len(self) % 2 == 0:
                    milieu = len(self.name) / 2
                    milieu = int(milieu)
                    print(milieu)
                    self.firstName = self.name[0:milieu]
                    self.lastName = self.name[milieu + 1:len(self.name)]
                    print(self.firstName, self.lastName)
                else:
                    leng = len(self.name) + 1
                    milieu = (leng / 2)
                    milieu = int(milieu)
                    print(milieu)
                    self.firstName = self.name[0:milieu]
                    self.lastName = self.name[milieu:len(self.name)]
                    print(self.firstName, self.lastName)

            # Récuperer le mot de passe à partir de res.users
            user = self.env['res.users'].sudo().search([('partner_id', 'in', self.ids)])
            if user:
                self.password360 = user.password360
                print(user.password)
                id_Digimoov_bienvenue = '56f5520e11d423f46884d594'
                company_id = '56f5520e11d423f46884d593'
                api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
                urluser = 'https://app.360learning.com/api/v1/users?company=' + company_id + '&apiKey=' + api_key
                urlgroup = 'https://app.360learning.com/api/v1/groups/' + id_Digimoov_bienvenue + '/users/' + self.email + '?company=' + company_id + '&apiKey=' + api_key

                headers = CaseInsensitiveDict()
                headers["Content-Type"] = "application/json"

                data = '{"mail":"' + self.email + '" , "password":"' + self.password360 + '" , "firstName":"' + self.firstName + '" , "lastName":"' + self.lastName + '"}'
                print(data)
                #Ajouter i-One à table user
                resp = requests.post(urluser, headers=headers, data=data)
                print(resp.status_code)
                if (resp.status_code == 200):
                    user.password360 = ""
                    self.apprenant=True

                # Affecter i-One au groupe digimoov-bienvenue
                data_group = {}
                respgroupe = requests.put(urlgroup, headers=headers, data=data_group)
                print('groupe', respgroupe.status_code)

    def delete(self):
     company_id = '56f5520e11d423f46884d593'
     api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
     headers = CaseInsensitiveDict()
     headers["Accept"] = "*/*"
     email = self.email
     url = "https://app.360learning.com/api/v1/users/"+ email +"?company=" + company_id + "&apiKey=" + api_key
     resp = requests.delete(url)

     print(resp.status_code)
