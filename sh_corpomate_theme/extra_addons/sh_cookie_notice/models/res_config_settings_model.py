# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import api, fields, models


class website(models.Model):
    _inherit = 'website'

    sh_is_cookie_notice=fields.Boolean(string="Cookie Notice")   
    sh_message=fields.Text(string="Message", default="This website uses cookies to ensure you get the best experience on our website.",translate=True)
    sh_btn_text=fields.Char(string="Button Text", default="Got It",translate=True)
    sh_policy_link_text=fields.Char(string="Policy Link Text", default="Learn more",translate=True)
    sh_policy_url=fields.Char(string="Policy URL")
    sh_position=fields.Selection([
        ('bottom','Banner bottom'),
        ('top','Banner Top'),
        ('bottom-left','Floating left'),
        ('bottom-right','Floating right'),
        ('static_top','Banner top (pushdown)'),
        ],string="Position",default='bottom')

class res_config_settings(models.TransientModel):
    _inherit="res.config.settings"
    
    sh_is_cookie_notice=fields.Boolean(related="website_id.sh_is_cookie_notice",string="Cookie Notice",readonly=False)
    sh_message=fields.Text(related="website_id.sh_message", string="Message", readonly=False)
    sh_btn_text=fields.Char(related="website_id.sh_btn_text", string="Button Text", readonly=False)
    sh_policy_link_text=fields.Char(related="website_id.sh_policy_link_text", string="Policy Link Text", readonly=False)
    sh_policy_url=fields.Char(related="website_id.sh_policy_url", string="Policy URL", readonly=False)
    sh_position=fields.Selection([
        ('bottom','Banner bottom'),
        ('top','Banner Top'),
        ('bottom-left','Floating left'),
        ('bottom-right','Floating right'),
        ('static_top','Banner top (pushdown)'),
        ],string="Position",related="website_id.sh_position", readonly=False)
    
    
