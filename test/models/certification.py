from datetime import timedelta
import requests
from odoo import models, fields, api, exceptions


class Certification(models.Model):
    _name = 'test.certification'
    _description = 'liste des certifications '