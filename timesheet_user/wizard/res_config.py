# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    api_url = fields.Char(related="company_id.api_url", readonly=False)
    api_db = fields.Char(related="company_id.api_db", readonly=False)
    api_username = fields.Char(related="company_id.api_username", readonly=False)
    api_password = fields.Char(related="company_id.api_password", readonly=False)
