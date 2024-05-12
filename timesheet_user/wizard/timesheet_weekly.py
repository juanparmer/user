# -*- coding: utf-8 -*-

import base64

from odoo import _, fields, models
from odoo.exceptions import UserError


class TimesheetWeekly(models.TransientModel):
    _name = 'timesheet.weekly'
    _description = 'Weekly Timesheet'

    company_id = fields.Many2one(
        comodel_name='res.company',
        default=lambda self: self.env.company
    )

    email_type = fields.Selection(
        selection=[
            ('compose', 'Single'),
            ('message', 'Multi-Project')
        ],
        default='compose',
        required=True
    )

    date_start = fields.Date(
        string='Start date',
        required=True
    )
    date_end = fields.Date(
        string='End date',
        required=True
    )

    project_id = fields.Many2one('project.project')
    projects_ids = fields.Many2many('project.project')

    def action_confirm(self):
        self.ensure_one()
        return getattr(self, 'action_confirm_%s' % self.email_type)()

    def action_confirm_compose(self):
        self.ensure_one()

        Attachment = self.env['ir.attachment']
        Report = self.env['ir.actions.report']
        Timesheet = self.env['account.analytic.line']

        report = self.env.ref('hr_timesheet.timesheet_report')
        subtype = self.env.ref('timesheet_user.mail_message_subtype_timesheet')
        template = self.env.ref('timesheet_user.template_timesheet_weekly')
        view = self.env.ref('mail.email_compose_message_wizard_form')

        button_name = _('Send Mail (%s)', template.name)
        # Timesheets
        timesheets = Timesheet.search([
            ('project_id', '=', self.project_id.id),
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_end),
        ])
        if not timesheets:
            raise UserError(
                'Project does not have hours registered for the specified dates.'
            )
        # attachment_ids
        report_content, report_format = Report._render_qweb_pdf(
            report, timesheets.ids
        )
        report_content = base64.b64encode(report_content)
        report_name = '%s Timesheet Report (%s)' % (
            self.project_id.partner_id.name,
            (fields.Date.to_string(self.date_end)),
        )
        extension = "." + report_format
        report_name += extension
        attachment_data = {
            'name': report_name,
            'datas': report_content,
            'type': 'binary',
            'res_model': 'mail.compose.message',
            'res_id': 0
        }
        attachment = Attachment.create(attachment_data)
        # Action
        context = {
            # 'default_composition_mode': 'mass_mail',
            'default_model': template.model,
            'default_res_ids': self.project_id.ids,
            'default_template_id': template.id,
            'default_subtype_id': subtype.id,
            'default_attachment_ids': [(4, attachment.id, 0)],
            # 'default_partner_ids': [(4, self.project_id.partner_id.id, 0)],
        }
        return {
            'name': button_name,
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'context': repr(context),
            'view_mode': 'form',
            'views': [(False, 'form')],
            'view_id': view.id,
            'target': 'new',
            'binding_model_id': template.model_id.id,
        }

    def action_confirm_message(self):
        self.ensure_one()

        Report = self.env['ir.actions.report']
        Timesheet = self.env['account.analytic.line']

        report = self.env.ref('hr_timesheet.timesheet_report')
        subtype = self.env.ref('timesheet_user.mail_message_subtype_timesheet')
        template = self.env.ref('timesheet_user.template_timesheet_weekly')

        project_names = []
        mail_ids = []
        # Project
        for project in self.projects_ids:
            # Timesheets
            timesheets = Timesheet.search([
                ('project_id', '=', project.id),
                ('date', '>=', self.date_start),
                ('date', '<=', self.date_end),
            ])
            if not timesheets:
                project_names.append(project.name)
                continue

        if project_names:
            messsage_error = 'The following projects do not have hours registered for the specified dates:'
            for project_name in project_names:
                messsage_error += '\n %s' % project_name
            raise UserError(messsage_error)

        for project in self.projects_ids:
            # Timesheets
            timesheets = Timesheet.search([
                ('project_id', '=', project.id),
                ('date', '>=', self.date_start),
                ('date', '<=', self.date_end),
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
                (fields.Date.to_string(self.date_end)),
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
            mail_id = template.send_mail(
                project.id,
                force_send=True,
                raise_exception=False,
                email_values=email_values,
                email_layout_xmlid=False
            )
            mail_ids.append(mail_id)

        # Action
        return {
            'name': _('Timesheet Emails'),
            'type': 'ir.actions.act_window',
            'res_model': 'mail.mail',
            'view_mode': 'tree, form',
            'views': [(False, 'tree'), (False, 'form')],
            'domain': [('id', 'in', mail_ids)],
            # 'target': 'current',
        }
