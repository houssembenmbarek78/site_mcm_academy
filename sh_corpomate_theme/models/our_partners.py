# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class sh_corpomate_theme_our_partner(models.Model):
    _name = "sh.corpomate.theme.our.partner"
    _description = "Our Partners Corpomate Theme"
    _order = "id desc"    
    
    
    name = fields.Many2one(comodel_name="res.partner",string = "Partner",required = True)    
    sequence = fields.Integer(string = "Sequence")
    active = fields.Boolean(string = "Active")
    image = fields.Binary(string = "Image")    
    
    @api.onchange('name')
    def _onchange_name(self):   
        if self.name:
            self.image =  self.name.image_1920      
            