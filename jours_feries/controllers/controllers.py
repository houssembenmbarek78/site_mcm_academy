# -*- coding: utf-8 -*-
# from odoo import http


# class JoursFeries(http.Controller):
#     @http.route('/jours_feries/jours_feries/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jours_feries/jours_feries/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('jours_feries.listing', {
#             'root': '/jours_feries/jours_feries',
#             'objects': http.request.env['jours_feries.jours_feries'].search([]),
#         })

#     @http.route('/jours_feries/jours_feries/objects/<model("jours_feries.jours_feries"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jours_feries.object', {
#             'object': obj
#         })
