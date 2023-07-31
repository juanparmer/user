# -*- coding: utf-8 -*-
# from odoo import http


# class MrpUser(http.Controller):
#     @http.route('/mrp_user/mrp_user', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_user/mrp_user/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_user.listing', {
#             'root': '/mrp_user/mrp_user',
#             'objects': http.request.env['mrp_user.mrp_user'].search([]),
#         })

#     @http.route('/mrp_user/mrp_user/objects/<model("mrp_user.mrp_user"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_user.object', {
#             'object': obj
#         })
