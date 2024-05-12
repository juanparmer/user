# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # timesheet_email_from = fields.Char(
    #     string='From',
    #     help="Sender address (placeholders may be used here). If not set, the default value will be the author's email alias if configured, or email address."
    # )
    # timesheet_email_to = fields.Char(
    #     string='To (Emails)',
    #     help="Comma-separated recipient addresses (placeholders may be used here)"
    # )
    timesheet_email_cc = fields.Char(
        string='Cc',
        help="Carbon copy recipients (placeholders may be used here)"
    )
    timesheet_report = fields.Boolean(
        default=False,
        copy=False
    )
