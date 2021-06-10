# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

from odoo.tools.translate import html_translate

class website_menu(models.Model):
    _inherit = "website.menu"
    
    sh_website_mega_menu_html = fields.Html(string = "Mega Menu", translate = html_translate)
    
    
    # method whcih redirect to frontend for design menu html structure
    def action_sh_design_mega_menu(self, context=None):
        
        if not len(self.ids) == 1:
            raise UserError(_('You can only design only one mega menu at a time.'))

        url = '/sh_website_megamenu/design_mega_menu?id=%d&enable_editor=1' % (self.id)
        return {
            'name': ('Edit Mega Menu'),
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }
            
    

            