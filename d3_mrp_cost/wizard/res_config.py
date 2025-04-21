# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    work_center_cost = fields.Boolean(
        related="company_id.work_center_cost", readonly=False
    )
