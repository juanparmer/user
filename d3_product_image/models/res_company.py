# -*- coding: utf-8 -*-


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    report_product_image = fields.Boolean(default=False)
    