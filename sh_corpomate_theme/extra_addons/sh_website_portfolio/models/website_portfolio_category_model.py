# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models,fields,api

class website_portfolio_category(models.Model):
    _name="website.portfolio.category"
    _description = "Website Portfolio Category"        
    
    name = fields.Char(string="Category", required=True, translate=True)
    is_active = fields.Boolean(string="Active",default=True)
    website_id = fields.Many2one('website', required=True)        
    