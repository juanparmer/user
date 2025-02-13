# -*- coding: utf-8 -*-

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.constrains("task_id", "helpdesk_ticket_id")
    def _check_no_link_task_and_ticket(self):
        return False
        # Check if any timesheets are not linked to a ticket and a task at the same time
        if any(
            timesheet.task_id and timesheet.helpdesk_ticket_id for timesheet in self
        ):
            raise ValidationError(
                _(
                    "You cannot link a timesheet entry to a task and a ticket at the same time."
                )
            )

    @api.onchange("helpdesk_ticket_id")
    def _onchange_helpdesk_ticket_id(self):
        if not self.task_id and self.helpdesk_ticket_id and self.project_id:
            self.task_id = self.project_id.helpdesk_task_id
