# -*- coding: utf-8 -*-
# from odoo import http


# class Ocrdocument(http.Controller):
#     @http.route('/ocrdocument/ocrdocument/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ocrdocument/ocrdocument/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ocrdocument.listing', {
#             'root': '/ocrdocument/ocrdocument',
#             'objects': http.request.env['ocrdocument.ocrdocument'].search([]),
#         })

#     @http.route('/ocrdocument/ocrdocument/objects/<model("ocrdocument.ocrdocument"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ocrdocument.object', {
#             'object': obj
#         })
