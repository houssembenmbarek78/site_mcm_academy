# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models

            
class website(models.Model):
    _inherit = "website"

    sh_wq_is_display_quote = fields.Boolean(string  = "Is Website Quote")
    
    sh_wq_quote_button_label = fields.Char(string  = "Button Label",
                                           default = "Get a Quote")
    
    sh_wq_quote_button_label_color = fields.Char(string  = "Button Label Color",
                                                 default = "#FFFFFF")
    
    sh_wq_quote_button_color = fields.Char(string  = "Button Color",
                                           default = "#000000")
    
    sh_wq_quote_button_position = fields.Selection([
        ('top-left','Top Left'),
        ('top-center','Top Center'),
        ('top-right','Top Right'),
        ('left','Mid Left'),
        ('center','Mid Center'),
        ('right','Mid Right'),
        ('bottom-left','Bottom Left'),
        ('bottom-center','Bottom Center'),
        ('bottom-right','Bottom Right'),
        ], default = 'bottom-right' , string = "Button Position")   
    
    sh_wq_quote_button_style = fields.Selection([
        ('fball','Bubble'),
        ('fbutton','Rectangle'),
        ],  string="Button Style",                                              
            default = "fball")       
    
    sh_wq_quote_bubble_image = fields.Binary(string  = "Bubble Image")       
    
    
    
    sh_wq_quote_bubble_hover_label = fields.Char(string  = "Bubble Hover Label",
                                                default = "Get a Quote")
    
    sh_wq_quote_bubble_hover_label_color = fields.Char(string  = "Bubble Hover Label Color",
                                                       default = "FFFFFF")
    
    sh_wq_quote_bubble_hover_color = fields.Char(string  = "Bubble Hover Background Color",
                                                default = "000000" )  
    
    
    #for field visibility
    sh_wq_is_contact_name = fields.Boolean(string  = "Your Name")
    sh_wq_is_phone = fields.Boolean(string  = "Phone Number")
    sh_wq_is_email_from = fields.Boolean(string  = "Email")
    sh_wq_is_partner_name = fields.Boolean(string  = "Your Company")
    sh_wq_is_name = fields.Boolean(string  = "Subject")
    sh_wq_is_description = fields.Boolean(string  = "Your question")
      
    

    
class res_config_settings(models.TransientModel):
    _inherit = "res.config.settings"


    sh_wq_is_display_quote = fields.Boolean(string  = "Is Website Quote",
                                            related="website_id.sh_wq_is_display_quote",
                                            readonly = False)
    
    sh_wq_quote_button_label = fields.Char(string  = "Button Label",
                                           related="website_id.sh_wq_quote_button_label",
                                           readonly = False)
    
    sh_wq_quote_button_label_color = fields.Char(string  = "Button Label Color",
                                           related="website_id.sh_wq_quote_button_label_color",
                                           readonly = False)   
    
    sh_wq_quote_button_color = fields.Char(string  = "Button Color",
                                           related="website_id.sh_wq_quote_button_color",
                                           readonly = False)  
    
    
    
    
    
    sh_wq_quote_button_position = fields.Selection([
        ('top-left','Top Left'),
        ('top-center','Top Center'),
        ('top-right','Top Right'),
        ('left','Mid Left'),
        ('center','Mid Center'),
        ('right','Mid Right'),
        ('bottom-left','Bottom Left'),
        ('bottom-center','Bottom Center'),
        ('bottom-right','Bottom Right'),
        ], string = "Button Position",
           related="website_id.sh_wq_quote_button_position",
           readonly = False)       
    
    
    sh_wq_quote_button_style = fields.Selection([
        ('fball','Bubble'),
        ('fbutton','Rectangle')
        ],  string="Button Style", 
            related="website_id.sh_wq_quote_button_style",                                               
            readonly = False)        
    
    sh_wq_quote_bubble_image = fields.Binary(string  = "Bubble Image",
                                           related="website_id.sh_wq_quote_bubble_image",
                                           readonly = False)
    
    sh_wq_quote_bubble_hover_label = fields.Char(string  = "Bubble Hover Label",
                                           related="website_id.sh_wq_quote_bubble_hover_label",
                                           readonly = False)  
    
    sh_wq_quote_bubble_hover_label_color = fields.Char(string  = "Bubble Hover Label Color",
                                           related="website_id.sh_wq_quote_bubble_hover_label_color",
                                           readonly = False)  
    
    sh_wq_quote_bubble_hover_color = fields.Char(string  = "Bubble Hover Background Color",
                                           related="website_id.sh_wq_quote_bubble_hover_color",
                                           readonly = False) 
    
    #for fields visibility
    sh_wq_is_contact_name = fields.Boolean(string  = "Your Name",
                                           related="website_id.sh_wq_is_contact_name",
                                           readonly = False) 
                                               
    sh_wq_is_phone = fields.Boolean(string  = "Phone Number",
                                           related="website_id.sh_wq_is_phone",
                                           readonly = False)     
    
    sh_wq_is_email_from = fields.Boolean(string  = "Email",
                                           related="website_id.sh_wq_is_email_from",
                                           readonly = False)     
    
    sh_wq_is_partner_name = fields.Boolean(string  = "Your Company",
                                           related="website_id.sh_wq_is_partner_name",
                                           readonly = False)     
    
    sh_wq_is_name = fields.Boolean(string  = "Subject",
                                           related="website_id.sh_wq_is_name",
                                           readonly = False)     
    
    sh_wq_is_description = fields.Boolean(string  = "Your question",
                                           related="website_id.sh_wq_is_description",
                                           readonly = False)     
       
    
            
    
      