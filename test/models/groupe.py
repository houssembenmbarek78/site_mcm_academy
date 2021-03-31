
from datetime import timedelta
import requests
from odoo import models, fields, api, exceptions
from datetime import datetime


class Groupe(models.Model):
    _name = 'test.groupe'
    _description = 'liste des groupes '
    id_groupe = fields.Char(string="id_groupe")
    name = fields.Char(string="Nom", require=True)
    description = fields.Char(string="Description")
    public = fields.Boolean(string="Public")
    parent_id = fields.Many2one('test.groupe',ondelete='set null', string="Groupe Parent")
    # children_id = fields.One2many('test.groupe', 'parent_id', string='Sous groupes')
    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True)
    admins_ids = fields.Many2many('res.partner' ,relation='admins_ids', string='Les Admins')
    # authors_ids = fields.Many2many('res.users', string='Les Auteurs')
    users_ids = fields.Many2many('res.partner',relation='users_ids', string='Les Apprenants',
                                 domain=[
                                         ('apprenant', '=', True)
                                 ])
    # coaches_ids = fields.Many2many('res.partner', string='Les Coachs')
    users_count = fields.Integer(string="Apprenants", compute="_get_ione_count",store=True)

    session_ids = fields.One2many(
        'test.session', 'groupe_id', string="Sessions")
    parcours_ids = fields.One2many('test.parcours', 'groupe_id', string="Parcours")
    parcours_count = fields.Integer(string="Nb.Parcours", compute="_getParcours_count")

    # @api.constrains('admins_ids', ' coaches_ids')
    # def _check_instructor_not_in_attendee(self):
    #     for record in self:
    #         if record.coaches_ids and record.coaches_ids in record.admins_ids:
    #             raise exceptions.ValidationError("Un coache ne peut pas etre un admininistrateur")

    # Methode de calcule de nombre de Parcours:
    @api.depends('parcours_ids')
    def _getParcours_count(self):
        for record in self:
            record.parcours_count = len(record.parcours_ids)

   #Methode cron pour recupérer parcours et groupe à partir de 360
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

            find_groupe = self.env['test.groupe'].sudo().search([('name', "=", namegroupe)])
            if not (find_groupe):
                vals = {
                    'id_groupe': id_groupe,
                    'name': groupe['name'],
                    'public': groupe['public']
                }
                self.env['test.groupe'].create(vals)
                print(vals)

            resparcours = requests.get('https://app.360learning.com/api/v1/groups/' + id_groupe + '/programs',
                                       params=params)
            for parcours in resparcours.json():
                startDate = str(parcours['startDate'])
                start_Date = ""
                endDate = str(parcours['endDate'])
                end_Date = ""
                if len(endDate) > 0:
                    date_split = endDate[0:19]
                    date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                    new_format = '%d %B, %Y'
                    end_Date = date.strftime(new_format)

                if len(startDate) > 0:
                    date_split = startDate[0:19]
                    date = datetime.strptime(date_split, "%Y-%m-%dT%H:%M:%S")
                    new_format = '%d %B, %Y'
                    start_Date = date.strftime(new_format)

                durée = ''
                type_durée = ''
                if 'programDurationType' in parcours:
                    type_durée = parcours['programDurationType']
                if 'programDuration' in parcours:
                    durée = parcours['programDuration']
                print('parcours***************', len(resparcours.json()), parcours)
                name_parcours = parcours['name']
                if parcours:
                    parc = self.env['test.parcours'].sudo().search([('name', "=", name_parcours)])
                    if parc:
                        values = {
                            'id_parcours': parcours['_id'],
                            'name': parcours['name'],
                            'endDate': end_Date,
                            'startDate': start_Date,
                            'hasUserLimit': parcours['hasUserLimit'],
                            'programTemplate': parcours['programTemplate'],
                            'programDuration': durée,
                            'programDurationType': type_durée,
                            'group_id_plateforme': id_groupe
                        }
                        parc.sudo().write(values)
                        print(values)







  #Compter le nombre des clients
    @api.depends('users_ids')
    def _get_ione_count(self):
        for record in self:
            record.users_count = len(record.users_ids)

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

    # _sql_constraints = [
    #     ('check_description_name',
    #      'CHECK(name != description)',
    #      "Le nom doit etre différent de description",
    #      ),
    #     ('check_name',
    #      'UNIQUE(name)',
    #      "le nom doit etre unique",
    #      ),
    #     ('check_admin_coach',
    #      'CHECK(admins_ids != authors_ids)',
    #      "L\'admin doit etre différent d'auteur'",
    #      ),
    #     ('check_user_author',
    #      'CHECK(coaches_ids != users_ids)',
    #      "Le coach doit etre différent d\'utilisateur",
    #      ),
    # ]

   #Récuperer les groupes de 360
    def get_groupes(self):
     params = (
        ('company', '56f5520e11d423f46884d593'),
        ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
     )

     response = requests.get('https://app.360learning.com/api/v1/groups', params=params)
     for record in response.json():
        print("response........", record,len(response.json()))
