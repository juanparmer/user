# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    api_url = fields.Char()
    api_db = fields.Char()
    api_username = fields.Char()
    api_password = fields.Char()

    # def execute_fetchall(self, query):
    #     self.env.cr.execute(query)
    #     return self.env.cr.fetchall()

    # def execute_fetchone(self, query):
    #     self.env.cr.execute(query)
    #     return self.env.cr.fetchone()

    def execute_dictfetchall(self, query):
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    # def execute_dictfetchone(self, query):
    #     self.env.cr.execute(query)
    #     return self.env.cr.dictfetchone()
