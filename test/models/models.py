# -*- coding: utf-8 -*-
from datetime import timedelta
import requests
from odoo import models, fields, api, exceptions


class course(models.Model):
    _name = 'test.course'
    _description = 'OpenAcademy Courses'

    name = fields.Char(string="Nom", require=True)
    description = fields.Char(string="Description")

    responsible_id = fields.Many2one('res.users',
                                     ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many(
        'test.session', 'groupe_id', string="Sessions")

    def copy(self, default=None):
        default = (default or {})
        copied_count = self.search_count(
            [('name', '=like', u"copy of {}%".format(self.name))])
        if not copied_count:
            new_name = u"copy of {}%".format(self.name)
        else:
            new_name = u"copy of {}%".format(self.name, copied_count)
        default['name'] = new_name
        return super(course, self).copy(default)

    _sql_constraints = [
        ('check_description_name',
         'CHECK(name != description)',
         "Le nom doit etre différent de description",
         ),
        ('check_name',
         'UNIQUE(name)',
         "le nom doit etre unique",
         )
    ]


# --------------- modele session --------------------

class Session(models.Model):
    _name = "test.session"
    _description = "Session"
   #-------champs--------------

    name = fields.Char(required=True)
    date_debut = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="durée par jour")
    seats = fields.Integer(string="nombre des places")
    active = fields.Boolean(default=True)
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|',
                                            ('instructor', '=', True),
                                            ('category_id.name', 'ilike', "Teacher")]
                                    )
    groupe_id = fields.Many2one('test.groupe',
                                ondelete='cascade', string="Groupe", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Participants")

    taken_seats = fields.Float(string="Place Occupées", compute='_taken_seats')


    end_date = fields.Date(string="Date_de_fin", compute='_get_end_date',store=True, inverse='_set_end_date')
    attendee_count =fields.Integer(string="Nombre des Participants", compute='_get_attendees_count', store=True)
    color = fields.Integer()


    #----------------methodes----------
    @api.depends('date_debut', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.date_debut and r.duration):
                r.end_date = r.date_debut
                continue
            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds= -1)
            r.end_date = r.date_debut + duration

    def _set_end_date(self):
        for r in self:
            if not (r.end_date and r.date_debut):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.date_debut).days + 1



    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for record in self:
            record.attendee_count= len(record.attendee_ids)




    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': 'Valeur des Places incorrectee',
                    'message': 'Le nombre de places disponibles ne doit pas être négatif',
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': 'Trop de participants',
                    'message': 'Augmenter le nombre des places ou supprimer les participants en trop'

                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendee(self):
            for record in self:
             if record.instructor_id and record.instructor_id in record.attendee_ids:
                raise exceptions.ValidationError("Un inspecteur ne peut pas etre un participant")


def click():
 params = (
    ('company', '56f5520e11d423f46884d593'),
    ('apiKey', 'cnkcbrhHKyfzKLx4zI7Ub2P5'),
)

 response = requests.get('https://app.360learning.com/api/v1/users', params=params)
 for record in response.raw:
   print("response........", record)