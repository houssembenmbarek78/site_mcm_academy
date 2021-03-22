# -*- coding: utf-8 -*-

from odoo import models, fields, api
from cv2 import cv2



class ocrdocument(models.Model):
    _name = 'ocrdocument.ocrdocument'
    _description = 'ocrdocument.ocrdocument'

    name = fields.Char()
    description = fields.Char(string="description")
# Extract text from image with open cv into text
    def trycv(self):
        for r in self:


           print('it is working')
