# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class sh_corpomate_theme_testimonial(models.Model):
    _name = "sh.corpomate.theme.testimonial"
    _description = "Testimonial Front Theme Config"
    _order = "id desc"
    
    comment = fields.Text(string = "Testimonial", required = True)
    name = fields.Many2one(comodel_name="res.partner",string = "Partner",required = True)    
    function = fields.Char(string = "Job Position")
    url_video = fields.Char(string = "Video URL")
    sequence = fields.Integer(string = "Sequence")
    active = fields.Boolean(string = "Active")
    image = fields.Binary(string = "Image")

    @api.onchange('name')
    def _onchange_name(self):   
        if self.name:
            
            self.function = self.name.function
            self.image =  self.name.image_1920  
        