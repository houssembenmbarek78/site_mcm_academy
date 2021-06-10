# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.http import request
from datetime import datetime

class sh_website_quote(http.Controller):

    
    @http.route(['/sh_website_quote/contact_us'], type='json', auth="public",methods=['POST'], website=True)
    def website_quote(self, **post ):
            
        if post.get('name'):
            
            lead_vals = {
               'contact_name' : post.get('contact_name',False),
               'phone'        : post.get('phone',False),
               'email_from'   : post.get('email_from',False),
               'partner_name' : post.get('partner_name',False),               
               'name'         : post.get('name',False),
               'description'  : post.get('description',False),
                }
            
            crm_lead_obj = request.env['crm.lead']
            created_lead = crm_lead_obj.sudo().create(lead_vals)
            if created_lead:
                return True
            else:
                return False
        else:
            return False
                
