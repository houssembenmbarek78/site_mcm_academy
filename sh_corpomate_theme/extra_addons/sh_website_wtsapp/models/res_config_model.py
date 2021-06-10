# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
class WebisteConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'


    sww_is_wtsapp = fields.Boolean(related='website_id.sww_is_wtsapp',string="WhatsApp Chat", readonly = False) 
    sww_cn = fields.Char(related="website_id.sww_cn",string="WhatsApp Contact No", readonly = False)
    sww_chat = fields.Char(related="website_id.sww_chat",string="WhatsApp Group Chat", readonly = False)        
    sww_message = fields.Text(related="website_id.sww_message",string="WhatsApp Default Message", readonly = False)
    sww_link_btn_title = fields.Char(related="website_id.sww_link_btn_title", string="Button Title", readonly = False)    
    sww_banner_img = fields.Binary(related="website_id.sww_banner_img",string="Image", readonly = False)
    sww_type = fields.Selection(related="website_id.sww_type",string="Type", readonly = False)    
    sww_style = fields.Selection(related="website_id.sww_style",string="Style", readonly = False)    
    sww_position = fields.Selection(related="website_id.sww_position",string="Position", readonly = False)
    sww_color = fields.Char(related="website_id.sww_color",string="Background Color", readonly = False)
    sww_text_color = fields.Char(related="website_id.sww_text_color",string="Text Color", readonly = False)
            
class website(models.Model):
    _inherit = 'website'



    sww_is_wtsapp = fields.Boolean(string="WhatsApp Chat") 
    sww_cn = fields.Char(string="WhatsApp Contact No")
    sww_chat = fields.Char(string="WhatsApp Group Chat")        
    sww_message = fields.Text(string="WhatsApp Default Message")
    sww_link_btn_title = fields.Char(string="Link Button Name",translate=True)   
    sww_banner_img = fields.Binary(string="Image")   
    sww_style = fields.Selection([('fball','Floating Ball'),('fbutton','Floating Button')],string="Style",default='fball')    
    sww_position = fields.Selection([('top-left','Top Left'),('top-center','Top Center'),('top-right','Top Right'),('left','Mid Left'),('center','Mid Center'),('right','Mid Right'),('bottom-left','Bottom Left'),('bottom-center','Bottom Center'),('bottom-right','Bottom Right')],string="Position")    
    sww_type = fields.Selection([('chat','Group Chat'),('contact','Contact')],string="Type")   
    sww_color = fields.Char(string="Background Color",default = "4FCE5D")
    sww_text_color = fields.Char(string="Text Color",default = "FFFFFF")    
    

    