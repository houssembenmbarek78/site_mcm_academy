# -*- coding: utf-8 -*-

from odoo import models, fields, api
import cv2
import pytesseract



class ocrdocument(models.Model):
    _name = 'ocrdocument.ocrdocument'
    _description = 'ocrdocument.ocrdocument'

    name = fields.Char()
    description = fields.Char(string="description")

    def trycv(self):
        for r in self:
            img = cv2.imread('image.png')
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image=pytesseract.image_to_string(img)
            print(image)
            cv2.imshow('Result', img)
            cv2.waitKey(0)