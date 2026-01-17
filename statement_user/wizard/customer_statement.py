# -*- coding: utf-8 -*-

from odoo import fields, models


class StatementCustomerWizard(models.TransientModel):
    _name = "statement.customer.wizard"
    _description = "statement.customer.wizard"

    date_to = fields.Date()
    date_from = fields.Date()
