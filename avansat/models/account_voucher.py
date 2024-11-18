# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    avansat_id = fields.Many2one("avansat.avansat", copy=False)
