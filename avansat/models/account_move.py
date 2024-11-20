# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    avansat_id = fields.Many2one("avansat.avansat", copy=False)
