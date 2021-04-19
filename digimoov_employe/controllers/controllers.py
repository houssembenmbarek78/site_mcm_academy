# -*- coding: utf-8 -*-
# from odoo import http


# class DigimoovEmploye(http.Controller):
#     @http.route('/digimoov_employe/digimoov_employe/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/digimoov_employe/digimoov_employe/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('digimoov_employe.listing', {
#             'root': '/digimoov_employe/digimoov_employe',
#             'objects': http.request.env['digimoov_employe.digimoov_employe'].search([]),
#         })

#     @http.route('/digimoov_employe/digimoov_employe/objects/<model("digimoov_employe.digimoov_employe"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('digimoov_employe.object', {
#             'object': obj
#         })
