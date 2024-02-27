# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteUser(http.Controller):
#     @http.route('/website_user/website_user', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_user/website_user/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_user.listing', {
#             'root': '/website_user/website_user',
#             'objects': http.request.env['website_user.website_user'].search([]),
#         })

#     @http.route('/website_user/website_user/objects/<model("website_user.website_user"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_user.object', {
#             'object': obj
#         })

