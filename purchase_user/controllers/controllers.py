# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseUser(http.Controller):
#     @http.route('/purchase_user/purchase_user', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_user/purchase_user/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_user.listing', {
#             'root': '/purchase_user/purchase_user',
#             'objects': http.request.env['purchase_user.purchase_user'].search([]),
#         })

#     @http.route('/purchase_user/purchase_user/objects/<model("purchase_user.purchase_user"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_user.object', {
#             'object': obj
#         })
