# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.



from odoo import http
from odoo.http import request


class MegaMenuController(http.Controller):


    @http.route('/sh_website_megamenu/design_mega_menu', type='http', auth="user", website=True)
    def design_mega_menu(self, id = False, **kw):
            
            if id and type(id) != int:
                id = int(id)
                
            
            record = False
            if id:
                record = request.env["website.menu"].browse(id)
            
            values = {
                'record': record,
            }
            return request.render("sh_corpomate_theme.sh_website_megamenu_design_mega_menu_tmpl",values)   
        

