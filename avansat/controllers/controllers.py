# -*- coding: utf-8 -*-
# from odoo import http


# class Avansat(http.Controller):
#     @http.route('/avansat/avansat', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/avansat/avansat/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('avansat.listing', {
#             'root': '/avansat/avansat',
#             'objects': http.request.env['avansat.avansat'].search([]),
#         })

#     @http.route('/avansat/avansat/objects/<model("avansat.avansat"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('avansat.object', {
#             'object': obj
#         })
