# -*- coding: utf-8 -*-

from odoo import _, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal account to relate advance',
        help='Account journal to relate advances'
    )
    advance_req_in_immediate_pay = fields.Boolean(
        'Advance required in immediate payment',
        help='Request an advance to confirm a sales '
        'order with immediate payment term.'
    )

    active_payment_advance = fields.Boolean(
        'Active payment advance',
        help='Activate functionality and  '
        'restrictions for advance payments.'
    )

    voucher_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Advance account',
        help='Account for the difference in payments.'
    )
