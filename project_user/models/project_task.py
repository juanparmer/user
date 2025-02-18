# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    user_stage_type_id = fields.Many2one(
        comodel_name="project.task.type",
        string="User Stage",
        compute="_compute_user_stage_type_id",
        inverse="_inverse_user_stage_type_id",
        store=True,
    )

    def _compute_user_stage_type_id(self):
        for task in self:
            task.user_stage_type_id = False

    def _inverse_user_stage_type_id(self):
        Personal = self.env["project.task.stage.personal"].sudo()
        user_id = self.env.context.get("default_user_id")
        for task in self:
            domain = [("task_id", "=", task.id), ("user_id", "=", user_id)]
            personal = Personal.search(domain)
            personal.stage_id = task.user_stage_type_id
