# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError


class Slider(models.Model):
    _name = "sh.corpomate.blog.slider"
    _description = "Slider"
    
    name = fields.Char(string = "Name", required = True)

    
    filter_type = fields.Selection([
        ('domain','Domain'),
        ('manual','Manually')
        ],default = "manual", string = "Filter Type", required = True)


    tab_blog_post_line = fields.One2many(comodel_name="sh.corpomate.blog.slider.tab.blog.post.line",inverse_name="slider_id", string = "Blog Post Tabs")

    is_show_tab = fields.Boolean(string = "Show Tabs?", default = True) 
    
    #OWL OPTIONS
    items = fields.Integer(string='Items Per Slide', required = True, default = 4)
    autoplay = fields.Boolean(string = "Automatic Slide?", default = True)
    speed = fields.Integer(string = "Slide Speed", default = 300)
    loop = fields.Boolean(string = "Loop Slide?", default = True)
    nav = fields.Boolean(string = "Show Navigation Buttons?", default = True)
    

          
    

            
class SliderTabBlogPostLine(models.Model):
    _name = "sh.corpomate.blog.slider.tab.blog.post.line"
    _description = "Blog Post Slider Tab"  
    _order = "sequence, id"    
    
    name = fields.Char(string = "Tab Name",required = True)
    blog_post_ids = fields.Many2many(comodel_name="blog.post", string = "Blog Posts")
    filter_id = fields.Many2one(comodel_name="ir.filters", string = "Filter", domain='[("model_id","=","blog.post" )]')    
    slider_id = fields.Many2one('sh.corpomate.blog.slider', string='Slider Reference', required=True, ondelete='cascade', index=True, copy=False)            
    sequence = fields.Integer('Display order')    
    limit = fields.Integer(string = "Limit")
    
    @api.onchange('limit')
    def _onchange_limit(self):
        if self.limit and self.limit < 0:
            raise ValidationError(_('Limit must not be negative.'))  
        
            
        
    