# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    project_id = fields.Many2one(
        comodel_name="project.project",
        related=False,
        readonly=False,
        store=True,
        tracking=True,
    )
    helpdesk_task_id = fields.Many2one(
        related="project_id.helpdesk_task_id",
        readonly=True,
    )

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self = self.sudo()
        project_ids = self.partner_id.commercial_partner_id.project_ids.filtered(
            lambda p: not p.stage_id.fold
        )
        if project_ids:
            self.project_id = project_ids[0]

    @api.model_create_multi
    def create(self, list_value):
        tickets = super(HelpdeskTicket, self).create(list_value)
        for ticket in tickets.filtered(lambda t: t.partner_id):
            ticket = ticket.sudo()
            project_ids = ticket.partner_id.commercial_partner_id.project_ids.filtered(
                lambda p: not p.stage_id.fold
            )
            if project_ids:
                ticket.project_id = project_ids[0]
            else:
                ticket.project_id = ticket.team_id.project_id
        return tickets
