# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
from odoo import api, fields, models, _

mime_selection = [ ('image/png', 'image/png'),('image/x-icon', 'image/x-icon'), ('image/gif', 'image/gif')]
display_selection = [('fullscreen', 'Fullscreen'), ('standalone', 'Standalone'), ('minimal-ui', 'Minimal')]
orientation_selection = [('landscape', 'Always Landscape')]

class PWAFrontendConfig(models.Model):
    _name = 'sh.pwa.frontend.config'
    _description = 'PWA Configuration'

    name = fields.Char(required=True, default='Softhealer')
    short_name = fields.Char(required=True, default='Softhealer')
    description = fields.Char(default='Softhealer App')
    theme_color = fields.Char(default='#DBDCDE')
    background_color = fields.Char(default='#3367D6')
    display = fields.Selection(selection=display_selection, default='fullscreen', required=True)
    orientation = fields.Selection(selection=orientation_selection)
    icon_small = fields.Binary(help='Set a small app icon. Must be at least 32x32 pixels')
    icon_small_mimetype = fields.Selection(selection=mime_selection, help='Set the mimetype of your small icon.')
    icon_small_size = fields.Char(default='32x32')
    icon = fields.Binary(help='Set a big app icon. Must be at least 512x512 pixels')
    icon_mimetype = fields.Selection(selection=mime_selection, help='Set the mimetype of your icon.')
    icon_size = fields.Char(default='512x512')
    start_url = fields.Char("Start URL", default='/')
    icon_iphone = fields.Binary(help='Icon for Iphone',string="Icon for Iphone")
    @api.model
    def default_get(self,default_fields):
        """ 
            Get Default Settings.
             
        """
        res = super(PWAFrontendConfig, self).default_get(default_fields)
         
        record = self.search_read([
            ('name','=','sh_pwa_frontend_config')
            ],limit = 1, order="id desc")
        
         
        if record:
            res.update(record[0])
                  
        return res
