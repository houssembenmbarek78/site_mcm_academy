# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict

from odoo import http, fields, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import html2plaintext


class website_portfolio(http.Controller):
    @http.route([
        '/page/portfolio',
    ], type='http', auth="public", website=True)
    def portfolio(self, **post):
           
        search_portfolio = False
        search_categories = False
        if request.website:
            portfolio_obj = request.env['website.portfolio']
            portfolio_category_obj = request.env['website.portfolio.category']
            
            search_portfolio = portfolio_obj.search([
                                    ('is_active','=',True),
                                    ('website_id', '=', request.website.id)
                                    ]);
            search_categories = portfolio_category_obj.search([
                                    ('is_active','=',True),
                                    ('website_id', '=', request.website.id)                                 
                                    ]);

        return request.render("sh_corpomate_theme.portfolio", {'portfolio':search_portfolio,'categories':search_categories})
    
    
    
    
    
    
    