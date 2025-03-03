# -*- coding: utf-8 -*-

from odoo import fields, models


class ProjectProjectUser(models.TransientModel):
    _name = "project.task.user"
    _description = "Project User Tasks"

    user_id = fields.Many2one("res.users")

    def action_confirm(self):
        action = self.env.ref("project_user.project_task_action")
        action = action.sudo().read()[0]

        user_id = self.user_id.id
        domain = [("user_ids", "in", [user_id])]
        context = {
            "search_default_open_tasks": 1,
            "all_task": 0,
            "default_user_ids": [(4, user_id)],
            "default_user_id": user_id,
        }

        action.update({"domain": domain, "context": context})

        self.compute_user_stage()

        return action

    def compute_user_stage(self):
        Personal = self.env["project.task.stage.personal"].sudo()
        Task = self.env["project.task"].sudo()

        user_id = self.user_id.id

        domain = [("user_ids", "in", [user_id])]
        tasks = Task.search(domain)

        domain = [("task_id", "in", tasks.ids), ("user_id", "=", user_id)]
        personals = Personal.search(domain)

        for task in tasks:
            personal = personals.filtered(lambda p: p.task_id.id == task.id)
            task.user_stage_type_id = personal.stage_id
