# -*- coding: utf-8 -*-
# from odoo import http


# class WebUser(http.Controller):
#     @http.route('/web_user/web_user', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/web_user/web_user/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('web_user.listing', {
#             'root': '/web_user/web_user',
#             'objects': http.request.env['web_user.web_user'].search([]),
#         })

#     @http.route('/web_user/web_user/objects/<model("web_user.web_user"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('web_user.object', {
#             'object': obj
#         })

