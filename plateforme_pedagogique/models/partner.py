import functools
import xmlrpc.client
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime,timedelta,date
import re
import json
from odoo import _
import locale

from odoo import models, fields,api
from odoo.exceptions import ValidationError
from unidecode import  unidecode
import logging
_logger = logging.getLogger(__name__)

class partner(models.Model):
    _inherit = 'res.partner'

    # ajouter champs au modele partner par defaut res.partner ne sont pas des instructors

    apprenant = fields.Boolean("Apprenant sur 360")
    group_id = fields.Many2many('plateforme_pedagogique.groupe', string="Groupe")
    # champs pour recuperer les statistiques
    assignedPrograms = fields.Integer(string='Nombre de programmes attribués')

    last_login = fields.Char(string="Derniere Activité", readonly=True)
    # learner_achivement=fields.Char(string="Réalisations des apprenants")
    averageScore = fields.Integer(string="Score Moyen", readonly=True)
    totalTimeSpentInMinutes = fields.Char(string="temps passé en minutes", readonly=True)
    password360 = fields.Char()  # Champs pour stocker le mot de passe non crypté
    firstName = fields.Char()
    lastName = fields.Char()
    date_creation=fields.Char(string="Date d'inscription")
    messages = fields.Char(string='Messages Postés')
    publications = fields.Char(string='Cours ou programmes publiés')
    comments = fields.Char(string='Commentaires Postés')
    reactions =fields.Char(string="Réactions dans les forums d'activités")
    renounce_request = fields.Boolean("Renonciation au droit de rétractation conformément aux dispositions de l'article L.221-28 1°")
    toDeactivateAt=fields.Char("Date de suppression")
    passage_exam=fields.Boolean("Examen passé",default=False)
    stats_ids=fields.Many2one('plateforme_pedagogique.user_stats')

    # Recuperer les utilisateurs de 360learning
    def getusers(self):
            locale.setlocale(locale.LC_TIME, str(self.env.user.lang) + '.utf8')
            params = (
                ('company', '56f5520e11d423f46884d593'),
                ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
            )
            response = requests.get('https://app.360learning.com/api/v1/users', params=params)
            users = response.json()
            # Faire un parcours sur chaque user et extraire ses statistiques
            for user in users:
                iduser = user['_id']
                email = user['mail']
                response_user = requests.get('https://app.360learning.com/api/v1/users/' + iduser, params=params)
                table_user = response_user.json()
                lastlogin=""
                if 'lastLoginAt' in table_user:
                 lastlogin = str(table_user['lastLoginAt'])
                    
                print('user date supp', table_user['toDeactivateAt'])
                times = ''
                # Ecrire le temps récupéré de 360 sous forme d'heures et minutes
                if 'totalTimeSpentInMinutes' in table_user:
                    time = int(table_user['totalTimeSpentInMinutes'])
                    heure = time // 60
                    minute = time % 60
                    times = str(heure) + 'h' + str(minute) + 'min'
                    if (heure == 0):
                        times = str(minute) + 'min'
                        print(times)
                    if (minute == 0):
                        times = '0min'
                average = ''
                
                # Vérifier l'existance de champ dans table_user
                if 'averageScore' in table_user:
                    average = str(table_user['averageScore'])
                    print(average)
                # Si lastlogin n'est pas vide on change le format de date sous forme "01 mars, 2021"
                if (len(lastlogin) > 0):
                    date_split = lastlogin[0:19]
                    date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                    new_format = '%d %B, %Y'
                    new_format = '%d %B, %Y'
                    last_login = str(date.strftime(new_format))

                message="0"
                if ('messages' in table_user):
                    message=table_user['messages']
                publication=''
                if('publications'in table_user):
                    publication=table_user['publications']
                comment="0"
                if ('comments' in table_user):
                    comments=table_user['comments']
                reaction="0"
                if('reactions' in table_user):
                    reaction=table_user['reactions']
                # Chercher par email le meme client pour lui affecter les stats de 360
                partners = self.env['res.partner'].sudo().search([('email', "=", email)])
                for partner in partners:
                    if partners:
                        partner.sudo().write({
                            'last_login': last_login,
                            'averageScore': average,
                            'comments':comment,
                            'reactions':reaction,
                            'publications':publication,
                            'messages':message,
                            'totalTimeSpentInMinutes': times,
                            'assignedPrograms': table_user['assignedPrograms'],
                            'toDeactivateAt': table_user['toDeactivateAt'],
                            'apprenant': True

                        })
                        print("partner",partner.name, partner.last_login)

    # Recuperer les statistique par session de 360learning
    def getstats_session(self):
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        response = requests.get('https://app.360learning.com/api/v1/courses', params=params)
        sessions = response.json()
        # faire un parcours sur chaque user et extraie ses statistique
        for session in sessions:
            id= session['_id']
            re = requests.get('https://app.360learning.com/api/v1/courses/'+id+'/stats/youcefallahoum@gmail.com',
                      params=params)
            pogramstat=re.json()
            print("courses:", session['name'],'*******',pogramstat)

    #En cas de changement de statut de client cette methode est exécutée

    def write(self, vals):
        if 'statut' in vals:
            #Si statut annulé on supprime i-One
            if vals['statut'] == 'canceled':

                self.supprimer_ione_manuelle()
        record=super(partner, self).write(vals)
        return record

    #Ajouter ione manuellement
    def ajouter_iOne_manuelle(self):
        # _logger.info("++++++++++++Cron ajouter_iOne_manuelle++++++++++++++++++++++")
        sale_order = self.env['sale.order'].sudo().search([('partner_id', '=', self.id),
                                                           ('session_id', '=', self.mcm_session_id.id),
                                                           ('module_id', '=', self.module_id.id),
                                                           ('state', '=', 'sale'),
                                                           ], limit=1, order="id desc")
        print('sale order', sale_order.name)
        # Récupérer les documents et vérifier si ils sont validés ou non
        documents = self.env['documents.document'].sudo().search([('partner_id', '=', self.id)])
        document_valide = False
        count = 0
        for document in documents:
            if (document.state == "validated"):
                count = count + 1
                print('valide')
        print('count', count, 'len', len(documents))
        if (count == len(documents) and count != 0):
            # _logger.info("++++++++++++Cron DOC VALIDER++++++++++++++++++++++")
            document_valide = True
        # Vérifier si partner a choisi une formation et si ses documents sont validés
        if ((sale_order) and (document_valide)):
            # delai de retractation
            failure = sale_order.failures
            statut = self.statut
            # Vérifier si contrat signé ou non
            if (sale_order.state == 'sale' and self.passage_exam == False):
                # _logger.info("++++++++++++Cron sale contrat signé++++++++++++++++++++++")
                print('contrat signé')
                date_signature = sale_order.signed_on
                if ( (failure == True) and (statut == 'won')):
                    # _logger.info("++++++++++++Cron failure++++++++++++++++++++++")
                    print('it works')
                    self.ajouter_iOne(self)
                # Vérifier si delai de retractaion et demande de renoncer  ne sont pas coché,
                # si aujourd'hui est la date d'ajout,et si le statut est gagné
                # alors on ajoute l'apprenant à 360
                if ((failure == False) and (statut == 'won')):
                    # Calculer date d'ajout apres 14jours de date de signature
                    date_ajout = date_signature + timedelta(days=14)
                    today = datetime.today()
                    print('partner', self.name, 'sale_order', sale_order, 'date_ajout:', date_ajout, 'today:', today)
                    # Si l'apprenant n'a pas demander une renonce de delai de retractation
                    # il doit attendre 14jours pour etre ajouté
                    if (not (self.renounce_request) and (date_ajout <= today)):
                        print('not renonce', self.name, 'failure', failure, 'statut', self.statut, 'date_ajout',
                              date_ajout)
                        self.ajouter_iOne(self)
                    # Si demande de renonce est coché donc l'apprenant est ajouté sans attendre 14jours
                    if (self.renounce_request):
                        print('renonce', self.name, 'failure', failure, 'statut', self.statut, 'date_ajout',
                              date_ajout)
                        self.ajouter_iOne(self)


    # Ajouter i-One sur 360learning après 14jours
    # si Délai de rétractation n'est pas coché
    def Ajouter_iOne_auto(self):
      for partner in self.env['res.partner'].sudo().search([('statut', "=", "won")]):
        #Pour chaque apprenant extraire le delai de retractation
        sale_order = self.env['sale.order'].sudo().search([('partner_id', '=', partner.id),
                                                           ('session_id', '=', partner.mcm_session_id.id),
                                                           ('module_id', '=', partner.module_id.id),
                                                           ('state', '=', 'sale'),
                                                           ('session_id.date_exam', '>', date.today())
                                                           ], limit=1,order="id desc")

        print('sale order',sale_order.name)
        #Récupérer les documents et vérifier si ils sont validés ou non
        documents = self.env['documents.document'].sudo().search([('partner_id','=',partner.id)])
        document_valide=False
        count=0
        for document in documents:
            if (document.state == "validated"):
                count=count+1
                print('valide')
        print('count',count,'len',len(documents))
        if (count == len(documents) and count!=0):
            document_valide=True
        # Vérifier si partner a choisi une formation et si ses documents sont validés
        if ((sale_order) and(document_valide)):
            #delai de retractation
            failure = sale_order.failures
            statut = partner.statut
            # Vérifier si contrat signé ou non
            if (sale_order.state == 'sale' and partner.passage_exam == False):
              print('contrat signé')
              date_signature = sale_order.signed_on
              if (failure == True):
                    print('it works')
                    self.ajouter_iOne(partner)
              #Vérifier si delai de retractaion et demande de renoncer  ne sont pas coché,
              # si aujourd'hui est la date d'ajout,et si le statut est gagné
              # alors on ajoute l'apprenant à 360
              else:
                    # Calculer date d'ajout apres 14jours de date de signature
                    date_ajout = date_signature + timedelta(days=14)
                    today = datetime.today()
                    print('partner', partner.name, 'sale_order', sale_order, 'date_ajout:', date_ajout, 'today:', today)
                    #Si l'apprenant n'a pas demander une renonce de delai de retractation
                    #il doit attendre 14jours pour etre ajouté
                    if (not(partner.renounce_request) and (date_ajout <= today)):
                      print('not renonce',partner.name,'failure', failure, 'statut',partner.statut,'date_ajout',date_ajout)
                      self.ajouter_iOne(partner)
                    #Si demande de renonce est coché donc l'apprenant est ajouté sans attendre 14jours
                    if (partner.renounce_request):
                      print('renonce', partner.name, 'failure', failure, 'statut', partner.statut, 'date_ajout',  date_ajout )
                      self.ajouter_iOne(partner)



    def ajouter_iOne(self, partner):
        # Remplacez les paramètres régionaux de l'heure par le paramètre de langue actuel 
        # du compte dans odoo
        locale.setlocale(locale.LC_TIME, str(self.env.user.lang) + '.utf8')
        product_name = partner.module_id.product_id.name
        if (not (product_name)):
            product_name = ''
        if not (partner.phone):
            partner.phone = ''
        # Extraire firstName et lastName à partir du champs name
        self.diviser_nom(partner)
        ville = str(partner.mcm_session_id.ville).upper()
        new_format = '%d %B %Y'
        if (partner.mcm_session_id.date_exam):
            date_exam = partner.mcm_session_id.date_exam
            # Changer format de date et la mettre en majuscule
            datesession = str(date_exam.strftime(new_format).upper())
            date_session = unidecode(datesession)
            # print('date, ville', ville, date_session)
            # Récuperer le mot de passe à partir de res.users
            user = self.env['res.users'].sudo().search([('partner_id', '=', partner.id)])

            if user:
                id_Digimoov_bienvenue = '56f5520e11d423f46884d594'
                id_Digimoov_Examen_Attestation = '5f9af8dae5769d1a2c9d5047'
                params = (
                    ('company', '56f5520e11d423f46884d593'),
                    ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
                )
                company_id = '56f5520e11d423f46884d593'
                api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
                urluser = 'https://app.360learning.com/api/v1/users?company=' + company_id + '&apiKey=' + api_key
                urlgroup_Bienvenue = 'https://app.360learning.com/api/v1/groups/' + id_Digimoov_bienvenue + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                url_groups = 'https://app.360learning.com/api/v1/groups'
                url_unsubscribeToEmailNotifications = 'https://app.360learning.com/api/v1/users/unsubscribeToEmailNotifications?company=' + company_id + '&apiKey=' + api_key
                headers = CaseInsensitiveDict()
                headers["Content-Type"] = "application/json"
                invit = False
                create = False
                # Si le mot de passe n'est pas récupérée au moment d'inscrit on invite l'apprennant
                # if user.password360==False:
                # data_user ='{"mail":"' + partner.email + '"}'
                # resp_invit = requests.post(urluser, headers=headers, data=data_user)
                # if(resp_invit.status_code == 200):
                #     invit=True
                # Si non si mot de passe récupéré on l'ajoute sur la plateforme avec le meme mot de passe
                if user.password360:
                    partner.password360 = user.password360
                    print(user.password)

                    # Ajouter i-One to table user
                    data_user = '{"mail":"' + partner.email + '" , "password":"' + user.password360 + '" , "firstName":"' + partner.firstName + '", "lastName":"' + partner.lastName + '", "phone":"' + partner.phone + '", "sendCredentials":"true"}'
                    resp = requests.post(urluser, headers=headers, data=data_user)
                    print(data_user, 'user', resp.status_code)
                    # _logger.info('_______________________Cron password360_________________________ %s' % data_user)
                    if (resp.status_code == 200):
                        create = True
                data_group = {}
                # Désactiver les notifications par email
                data_email = json.dumps({
                    "usersEmails": [
                        partner.email
                    ]
                })
                resp_unsub_email = requests.put(url_unsubscribeToEmailNotifications, headers=headers, data=data_email)
                print("desactiver email", resp_unsub_email.status_code)

                # Si l'apprenant a été ajouté sur table user on l'affecte aux autres groupes
                if (create):
                    today = date.today()
                    new_format = '%d %B %Y'
                    # Changer format de date et la mettre en majuscule
                    date_ajout = today.strftime(new_format)
                    partner.date_creation = date_ajout

                    # Affecter i-One to groupe digimoov-bienvenue
                    respgroupe = requests.put(urlgroup_Bienvenue, headers=headers, data=data_group)
                    print('bienvenue ', respgroupe.status_code, partner.date_creation)
                    partner.apprenant = True
                    # Affecter i-One à un pack et session choisi
                    response_grps = requests.get(url_groups, params=params)
                    existe = False
                    groupes = response_grps.json()
                    # print(response_grps.json())
                    company = str(partner.module_id.company_id.id)
                    for groupe in groupes:
                        # Convertir le nom en majuscule
                        nom_groupe = str(groupe['name']).upper()
                        print('nom groupe', groupe)
                        id_groupe = groupe['_id']
                        # affecter à groupe digimoov
                        digimoov_examen = "Digimoov - Attestation de capacité de transport de marchandises de moins de 3.5t"
                        # Si la company est digimoov on ajoute i-One sur 360
                        if (company == '2'):
                            if (nom_groupe == digimoov_examen.upper()):
                                urlsession = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respsession = requests.put(urlsession, headers=headers, data=data_group)
                                print("examen", 'ajouté à examen digimoov', respsession.status_code, 'groupe', nom_groupe)
                                print('groupe')
                                # Affecter à un pack solo
                            packsolo = "Digimoov - Pack Solo"
                            if (("solo" in product_name) and (nom_groupe == packsolo.upper())):
                                print(partner.module_id.name)
                                urlgrp_solo = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respgrp_solo = requests.put(urlgrp_solo, headers=headers, data=data_group)
                                print('affecté à solo', respgrp_solo.status_code)

                            # Affecter à un pack pro
                            pack_pro = "Digimoov - Pack Pro"
                            if (("pro" in product_name) and (nom_groupe == pack_pro.upper())):
                                print(partner.module_id.name)
                                urlgrp_pro = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respgrp_pro = requests.put(urlgrp_pro, headers=headers, data=data_group)
                                print('affecté à pro', respgrp_pro.status_code)

                            # Affecter à unpremium
                            packprem = "Digimoov - Pack Premium"
                            if (("premium" in product_name) and (nom_groupe == packprem.upper())):
                                print(partner.module_id.name)
                                urlgrp_prim = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respgrp_prim = requests.put(urlgrp_prim, headers=headers, data=data_group)
                                print('affecté à premium', respgrp_prim.status_code)

                            # Affecter apprenant à Digimoov-Révision
                            revision = "Digimoov - Repassage Examen"
                            if (("Repassage d'examen" in product_name) and (nom_groupe == revision.upper())):
                                urlgrp_revision = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respgrp_revision = requests.put(urlgrp_revision, headers=headers, data=data_group)
                                print('affecté à revision', respgrp_revision.status_code)

                            # Affecter apprenant à une session d'examen
                            print('date, ville', ville, date_session)
                            if (ville in nom_groupe) and (date_session in nom_groupe):
                                existe = True
                                urlsession = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respsession = requests.put(urlsession, headers=headers, data=data_group)
                                print(existe, 'ajouté à son session', respsession.status_code)

                  # Si la session n'est pas trouvée sur 360 on l'ajoute
                    print('exist', existe)
                    if not (existe):
                        nom = ville + ' - ' + date_session
                        nomgroupe = unidecode(nom)
                        print(nomgroupe)
                        urlgroups = 'https://app.360learning.com/api/v1/groups?company=' + company_id + '&apiKey=' + api_key
                        data_session = '{"name":"' + nomgroupe + '","parent":"' + id_Digimoov_Examen_Attestation + '"  , "public":"false" }'
                        create_session = requests.post(urlgroups, headers=headers, data=data_session)
                        print('creer  une session', create_session.status_code)
                        response_grpss = requests.get(url_groups, params=params)
                        groupess = response_grpss.json()
                        # print(response_grpss.json())
                        for groupe in groupess:
                            # Convertir le nom en majuscule
                            nom_groupe = str(groupe['name']).upper()
                            id_groupe = groupe['_id']
                            # Affecter apprenant à la nouvelle session d'examen
                            if (ville in nom_groupe) and (date_session in nom_groupe):
                                existe = True
                                urlsession = 'https://app.360learning.com/api/v1/groups/' + id_groupe + '/users/' + partner.email + '?company=' + company_id + '&apiKey=' + api_key
                                respsession = requests.put(urlsession, headers=headers, data=data_group)
                                print(existe, 'ajouter à son session', respsession.status_code)


    def supprimer_ione_auto(self):
     company_id = '56f5520e11d423f46884d593'
     api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
     headers = CaseInsensitiveDict()
     headers["Accept"] = "*/*"
     params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
     response = requests.get('https://app.360learning.com/api/v1/users', params=params)
     users = response.json()
     for user in users:
         iduser = user['_id']
         email = user['mail']
         #Pour chaque partner verifier si date_suppression est aujourd'hui
         # pour assurer la suppresion automatique
         partner= self.env['res.partner'].sudo().search([('email',"=",email)],limit=1)
         if(partner and partner.mcm_session_id.date_exam) :
             #date de suppression est date d'examen + 4jours
             date_suppression = partner.mcm_session_id.date_exam + timedelta(days=4)
             today = date.today()
             if(date_suppression <= today):
              email=partner['email']
              print('date_sup',email,date_suppression,today)
              url = 'https://app.360learning.com/api/v1/users/tmejri@digimoov.fr?company=' + company_id + '&apiKey=' + api_key
              resp = requests.delete(url)
              if resp.status_code==204:
                partner.passage_exam=True
                print('supprimé avec succès', resp.status_code,'passage',partner.passage_exam)
         else:
             print('date incompatible')

    def supprimer_ione_manuelle(self):
        company_id = '56f5520e11d423f46884d593'
        api_key = 'cnkcbrhHKyfzKLx4zI7Ub2P5'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "*/*"
        url = 'https://app.360learning.com/api/v1/users/'+ self.email +'?company=' + company_id + '&apiKey=' + api_key
        resp = requests.delete(url)
        if resp.status_code == 204:
            self.passage_exam = True
            print('supprimé avec succès', resp.status_code,'passage',self.passage_exam)

    # Extraire firstName et lastName à partir du champs name
    def diviser_nom(self, partner):
        # _logger.info('name au debut  %s' %partner.name)
        if partner.name == '':
            partner.firstName = partner.name
            partner.lastName = partner.name
        # Cas d'un nom composé
        else:
            if " " in partner.name:
                name = partner.name.split(" ", 1)
                if name:
                    partner.firstName = name[0]
                    partner.lastName = name[1]
                # _logger.info('name  last in  if name  %s'  % partner.name)
            # Cas d'un seul nom
            else:
                partner.firstName = partner.name
                partner.lastName = partner.name
                print('first', partner.firstName)

