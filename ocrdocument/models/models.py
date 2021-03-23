# -*- coding: utf-8 -*-

from odoo import models, fields, api
from cv2 import cv2
from pytesseract import pytesseract




class ocrdocument(models.Model):
    _name = 'ocrdocument.ocrdocument'
    _description = 'ocrdocument.ocrdocument'

    name = fields.Char()
    description = fields.Char(string="description")
# Extract text from image with open cv into text
    def trycv(self):
        for r in self:
           # img2 = cv2.imread('image.png')
           # cv2.imshow('Result2', img2)
           # cv2.waitKey(0)
           image = pytesseract.image_to_string('./image.png')
           print(image)
