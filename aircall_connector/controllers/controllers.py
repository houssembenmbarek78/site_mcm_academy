# -*- coding: utf-8 -*-
# from odoo import http


# class AircallConnector(http.Controller):
#     @http.route('/aircall_connector/aircall_connector/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aircall_connector/aircall_connector/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aircall_connector.listing', {
#             'root': '/aircall_connector/aircall_connector',
#             'objects': http.request.env['aircall_connector.aircall_connector'].search([]),
#         })

#     @http.route('/aircall_connector/aircall_connector/objects/<model("aircall_connector.aircall_connector"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aircall_connector.object', {
#             'object': obj
#         })
