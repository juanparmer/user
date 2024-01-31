# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    pac_journal_id = fields.Many2one('account.journal')
    pac_product_id = fields.Many2one('product.product')
