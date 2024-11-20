# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    avansat_id = fields.Many2one("avansat.avansat", copy=False)
