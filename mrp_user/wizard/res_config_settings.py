# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pac_journal_id = fields.Many2one(
        related='company_id.pac_journal_id', 
        readonly=False
    )
    pac_product_id = fields.Many2one(
        related='company_id.pac_product_id', 
        readonly=False
    )
