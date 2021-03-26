
from datetime import timedelta
import requests
from odoo import models, fields, api, exceptions


class Groupe(models.Model):
    _name = 'test.groupe'
    _description = 'liste des groupes '

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
    users_count = fields.Integer(string="Nombre d\'i-Ones", compute="_get_ione_count",store=True)

    session_ids = fields.One2many(
        'test.session', 'groupe_id', string="Sessions")

    # @api.constrains('admins_ids', ' coaches_ids')
    # def _check_instructor_not_in_attendee(self):
    #     for record in self:
    #         if record.coaches_ids and record.coaches_ids in record.admins_ids:
    #             raise exceptions.ValidationError("Un coache ne peut pas etre un admininistrateur")

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


    def click(self):
     params = (
        ('company', '56f5520e11d423f46884d593'),
        ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
     )

     response = requests.get('https://app.360learning.com/api/v1/groups', params=params)
     for record in response.json():
        print("response........", record,len(response.json()))
