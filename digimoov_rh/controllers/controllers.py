# -*- coding: utf-8 -*-
# from odoo import http


# class DigimoovRh(http.Controller):
#     @http.route('/digimoov_rh/digimoov_rh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/digimoov_rh/digimoov_rh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('digimoov_rh.listing', {
#             'root': '/digimoov_rh/digimoov_rh',
#             'objects': http.request.env['digimoov_rh.digimoov_rh'].search([]),
#         })

#     @http.route('/digimoov_rh/digimoov_rh/objects/<model("digimoov_rh.digimoov_rh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('digimoov_rh.object', {
#             'object': obj
#         })
