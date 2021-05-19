# -*- coding: utf-8 -*-
from datetime import timedelta
import requests
from odoo import models, fields, api, exceptions
from datetime import datetime


class Groupe(models.Model):
    _name = 'plateforme_pedagogique.groupe'
    _description = 'liste des groupes '
    
    id_groupe = fields.Char(string="id_groupe")
    name = fields.Char(string="Nom", require=True)
    description = fields.Char(string="Description")
    public = fields.Boolean(string="Public")
    parent_id = fields.Many2one('plateforme_pedagogique.groupe', ondelete='set null', string="Groupe Parent")
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True)
    admins_ids = fields.Many2many('res.users', string='Les Admins')
    partner_ids = fields.Many2many('res.partner', string='Les Apprenants', readonly=True)
    users_count = fields.Integer(string="i-Ones", compute="_get_ione_count", store=True)
    parcours_ids = fields.One2many('plateforme_pedagogique.parcours', 'groupe_id', string="Parcours")
    parcours_count = fields.Integer(string="Nb.Parcours", compute="_getParcours_count")

    def getParcours(self):
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        resgroupe = requests.get('https://app.360learning.com/api/v1/groups', params=params)
        for groupe in resgroupe.json():
            id_groupe = groupe['_id']
            namegroupe = groupe['name']
            print('groupe', groupe)
            resparcours = requests.get('https://app.360learning.com/api/v1/groups/' + id_groupe + '/programs',
                                       params=params)
            find_groupe = self.env['plateforme_pedagogique.groupe'].sudo().search([('name', "=", namegroupe)])
            if not (find_groupe):
               print('on ne doit pas créer un groupe',find_groupe)
               find_groupe=self.env['plateforme_pedagogique.groupe'].create({
                   'name': namegroupe,
               })
            if find_groupe:
             list = []
             for parcours in resparcours.json():
                startDate = str(parcours['startDate'])
                start_Date = ""
                endDate = str(parcours['endDate'])
                end_Date = ""
                if len(endDate) > 0:
                    date_split = endDate[0:19]
                    date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                    new_format = '%d %B, %Y, %H:%M:%S'
                    end_Date = date.strftime(new_format)
                if len(startDate) > 0:
                    date_split = startDate[0:19]
                    date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                    new_format =  '%d %B, %Y, %H:%M:%S'
                    start_Date = date.strftime(new_format)
                durée = ''
                type_durée = ''
                if 'programDurationType' in parcours:
                    type_durée = parcours['programDurationType']
                if 'programDuration' in parcours:
                    durée = parcours['programDuration']
                print('parcours***************', len(resparcours.json()), parcours)
                name_parcours = parcours['name']
                id_parcours = ['_id']
                if parcours:
                    start_date_string=str(start_Date)
                    exist = False
                    for parc_grp in find_groupe.parcours_ids:
                        # On compare le user d'api avec chaque user de groupe sur odoo si existant on l'ajoute à une liste
                        if ((parc_grp.startDate == start_date_string) and (parc_grp.name == name_parcours)):
                            exist = True
                            list.append(parc_grp.id)
                            print('exist', parc_grp.name , parc_grp.startDate)
                    # Apres le parcours si on a pas trouvé partner on doit verifier la table user
                    if not (exist):
                      print('n\'existe pas dans groupe')
                      find_parcours = self.env['plateforme_pedagogique.parcours'].sudo().search([('name', "=", name_parcours ),('startDate',"=",start_date_string)])
                      if not(find_parcours):
                        print('on ne doit pas créer parcours')
                      if (find_parcours):
                        print('existedans parcours',find_parcours.id)
                        list.append(find_parcours.id)
                        print('list',list)
                    find_groupe.sudo().write({
                            'parcours_ids': [(6,0,list)],
                        })

    # Récuperer les apprenants de chaque groupe
    def getusers_groupe(self):
        params = (
            ('company', '56f5520e11d423f46884d593'),
            ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
        )
        resgroupe = requests.get('https://app.360learning.com/api/v1/groups', params=params)
        # Parcours sur chaque groupe et reperer les données de chaque groupe
        for groupes in resgroupe.json():
            id_groupe = groupes['_id']
            namegroupe = groupes['name']
            print('groupe', groupes)
            resgroupes = requests.get('https://app.360learning.com/api/v1/groups/' + id_groupe ,
                                       params=params)
            groupe=resgroupes.json()
            # Verifier si le groupe existe sur odoo
            find_groupe = self.env['plateforme_pedagogique.groupe'].sudo().search([('name', "=", namegroupe)])
            if not (find_groupe):
                print('on ne  cree pas des groupe')
             # Si le groupe existe on fait un parcours sur les user de groupe d'api
            if (find_groupe):
                list = []
                print('findgroupe',find_groupe)
                users = groupe['users']
                for user in users:
                    # print('user',user)
                    id_user = user['_id']
                    mail=user['mail']
                    resuser = requests.get('https://app.360learning.com/api/v1/users/' + id_user, params=params)
                    table_user = resuser.json()
                    if table_user:
                     # chercher sur odoo les partners du groupe courant
                        exist = False
                        for partner_grp in find_groupe.partner_ids:
                             # On compare le user d'api avec chaque user de groupe sur odoo si existant on l'ajoute à une liste
                             if (partner_grp.email == mail):
                                exist=True
                                list.append(partner_grp.id)
                                print('exist',partner_grp.email)
                        #Apres le parcours si on a pas trouvé partner on doit verifier la table user
                        if not(exist):
                                 print('n\'existe pas')
                                 #Chercher partner dans res.users
                                 find_user = self.env['res.users'].sudo().search([('login', "=", mail)],limit=1)
                                 if not(find_user):
                                       print('not find user')
                                 #Si partner existe dans res.user et n'existe pas dans un groupe on l'affecte à la liste
                                 if (find_user):
                                     list.append(find_user.partner_id.id)
                                     print("list",list)
                                      #on remplace les partners du groupe trouvé par la liste des apprenants existant et non existant
                                     find_groupe.sudo().write({
                                      'partner_ids': [(6, 0,list )]
                                        })
    # Methode de calcule de nombre d'utilisateurs:
    @api.depends('partner_ids')
    def _get_ione_count(self):
        for record in self:
            record.users_count = len(record.partner_ids)

    # Methode de calcule de nombre de Parcours:
    @api.depends('parcours_ids')
    def _getParcours_count(self):
        for record in self:
            record.parcours_count = len(record.parcours_ids)

    def copy(self, default=None):
        default = (default or {})
        copied_count = self.search_count(
            [('name', '=like', u"copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"copy of {}%".format(self.name)
        else:
            new_name = u"copy of {}%".format(self.name, copied_count)
        default['name'] = new_name
        return super(Groupe, self).copy(default)








