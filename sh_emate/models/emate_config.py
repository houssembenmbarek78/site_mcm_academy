 # -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api,_
import base64
  
    
  
class sh_emate_config_settings(models.Model):
    _name = 'sh.emate.config.settings'
    _description = 'Emate Config Settings'    

    
    name = fields.Char(string="Emate Config Settings", default = "Mass Mailing Theme Settings")
        
    sh_emate_theme1_color_primary = fields.Char(string = "Primary")
    sh_emate_theme1_color_secondary =  fields.Char(string = "Secondary")
    sh_emate_theme1_color_extra_color_1 = fields.Char(string = "Extra Color 1")
    sh_emate_theme1_color_extra_color_2 = fields.Char(string = "Extra Color 2")
    sh_emate_theme1_color_extra_color_3 = fields.Char(string = "Extra Color 3")
    sh_emate_theme1_color_extra_color_4 = fields.Char(string = "Extra Color 4")

    sh_emate_theme1_color_text_header = fields.Char(string = "Header Text Color")
    sh_emate_theme1_color_text_content = fields.Char(string = "Content Text Color")
    
    

    def write(self,vals):
        """
           
           Write Theme Settings Data in sh_emate_variables.scss Attachment
        
        """
                
        res = super(sh_emate_config_settings,self).write(vals)
        if self: 
            for config in self:
                
                content = _('''
    $sh_emate_theme1_color_primary:%(sh_emate_theme1_color_primary)s;
    $sh_emate_theme1_color_secondary:%(sh_emate_theme1_color_secondary)s;
    $sh_emate_theme1_color_extra_color_1:%(sh_emate_theme1_color_extra_color_1)s;
    $sh_emate_theme1_color_extra_color_2:%(sh_emate_theme1_color_extra_color_2)s;
    $sh_emate_theme1_color_extra_color_3:%(sh_emate_theme1_color_extra_color_3)s;  
    $sh_emate_theme1_color_extra_color_4:%(sh_emate_theme1_color_extra_color_4)s;
    $sh_emate_theme1_color_text_header:%(sh_emate_theme1_color_text_header)s;
    $sh_emate_theme1_color_text_content:%(sh_emate_theme1_color_text_content)s;
    

                ''') % {
                    
                    'sh_emate_theme1_color_primary': config.sh_emate_theme1_color_primary,
                    'sh_emate_theme1_color_secondary': config.sh_emate_theme1_color_secondary,
                    'sh_emate_theme1_color_extra_color_1': config.sh_emate_theme1_color_extra_color_1,
                    'sh_emate_theme1_color_extra_color_2': config.sh_emate_theme1_color_extra_color_2,                   
                    'sh_emate_theme1_color_extra_color_3': config.sh_emate_theme1_color_extra_color_3,                                        
                    'sh_emate_theme1_color_extra_color_4': config.sh_emate_theme1_color_extra_color_4,
                    'sh_emate_theme1_color_text_header': config.sh_emate_theme1_color_text_header,                                        
                    'sh_emate_theme1_color_text_content': config.sh_emate_theme1_color_text_content,    
                                               
                }                
                
       
                
                IrAttachment = self.env["ir.attachment"]
                # search default attachment by url that will created when app installed...
                url = "/sh_emate/static/src/scss/sh_emate_variables.scss"        
                
                search_attachment = IrAttachment.sudo().search([
                    ('url','=',url),
                    ],limit = 1)
                
                print("\n\n\n content ==>",content)
                
                # Check if the file to save had already been modified
                datas = base64.b64encode((content or "\n").encode("utf-8"))
                if search_attachment:
                    # If it was already modified, simply override the corresponding attachment content
                    search_attachment.sudo().write({"datas": datas})     
                    
                else:
                    # If not, create a new attachment
                    new_attach = {
                        "name": "Emate Variables",
                        "type": "binary",
                        "mimetype": "text/scss",
                        "datas": datas,
                        "url": url,
                        "public": True,
                        "res_model": "ir.ui.view",
                        "store_fname": "sh_emate_variables.scss",
                    }

                    IrAttachment.sudo().create(new_attach)                    
                                   
                                        
                # clear the catch to applied our new theme effects.
                self.env["ir.qweb"].clear_caches()
                
        return res    
    
    
      