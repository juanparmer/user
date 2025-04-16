# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    api_url = fields.Char()
    api_db = fields.Char()
    api_username = fields.Char()
    api_password = fields.Char()
