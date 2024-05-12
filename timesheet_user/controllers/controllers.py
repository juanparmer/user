# -*- coding: utf-8 -*-
# from odoo import http


# class TimesheetUser(http.Controller):
#     @http.route('/timesheet_user/timesheet_user', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/timesheet_user/timesheet_user/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('timesheet_user.listing', {
#             'root': '/timesheet_user/timesheet_user',
#             'objects': http.request.env['timesheet_user.timesheet_user'].search([]),
#         })

#     @http.route('/timesheet_user/timesheet_user/objects/<model("timesheet_user.timesheet_user"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('timesheet_user.object', {
#             'object': obj
#         })

