# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request


class main(http.Controller):
    
    
    @http.route('/get_latest_news', type='json', auth="none")
    def get_latest_news(self, limit=False):
        latest_news_records =  request.env['sh.nb.notice.board'].sudo().search_read(
            domain = [('active','=',True)],
            fields = ['name','desc'],
            limit = limit,
            order = "id desc",
            )
        
        return latest_news_records

