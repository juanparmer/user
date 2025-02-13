# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    zoominfo_password = fields.Char(related='company_id.zoominfo_password', readonly=False)
    zoominfo_user = fields.Char(related='company_id.zoominfo_user', readonly=False)
