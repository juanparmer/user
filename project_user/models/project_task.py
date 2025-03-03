# -*- coding: utf-8 -*-

from odoo import api, fields, models

priority_color = {
    "1": 10,  # Green
    "2": 3,  # Yellow
    "3": 1,  # Red
    "4": 8,  # Blue
    "5": 5,  # Purple
}


class ProjectTask(models.Model):
    _inherit = "project.task"

    priority = fields.Selection(
        selection_add=[("2", "High"), ("3", "Very High")],
        ondelete={"2": "set default", "3": "set default"},
    )

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get("priority") and priority_color.get(vals.get("priority")):
    #             vals.update(color=priority_color.get(vals.get("priority")))
    #     return super(ProjectTask, self).create(vals_list)

    # def write(self, vals):
    #     if vals.get("priority") and priority_color.get(vals.get("priority")):
    #         vals.update(color=priority_color.get(vals.get("priority")))
    #     return super(ProjectTask, self).write(vals)

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
