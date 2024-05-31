# -*- coding: utf-8 -*-

import base64

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

    def run_timesheet_weekly(self):
        Report = self.env['ir.actions.report']
        Timesheet = self.env['account.analytic.line']

        report = self.env.ref('hr_timesheet.timesheet_report')
        subtype = self.env.ref('timesheet_user.mail_message_subtype_timesheet')
        template = self.env.ref('timesheet_user.template_timesheet_weekly')

        date_start = fields.Date.subtract(
            fields.Date.context_today(self), days=6
        )
        date_end = fields.Date.context_today(self)

        projects = self.search([('timesheet_report', '=', True)])
        for project in projects:
            # Timesheets
            timesheets = Timesheet.search([
                ('project_id', '=', project.id),
                ('date', '>=', date_start),
                ('date', '<=', date_end),
            ])
            if not timesheets:
                continue

            # attachment_ids
            report_content, report_format = Report._render_qweb_pdf(
                report, timesheets.ids
            )
            report_content = base64.b64encode(report_content)
            report_name = '%s Timesheet Report (%s)' % (
                project.partner_id.name,
                (fields.Date.to_string(date_end)),
            )
            extension = "." + report_format
            report_name += extension

            message_follower_ids = project.message_follower_ids.filtered(
                lambda m: subtype.id in m.subtype_ids.ids
            )

            email_values = {
                'attachments': [(report_name, report_content)],
                'recipient_ids': message_follower_ids.partner_id.ids,
                'subtype_id': subtype.id,
            }

            template.send_mail(
                project.id,
                force_send=True,
                raise_exception=False,
                email_values=email_values,
                email_layout_xmlid=False
            )

        return True
