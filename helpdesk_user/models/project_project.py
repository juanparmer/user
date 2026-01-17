# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    helpdesk_task_id = fields.Many2one(
        comodel_name="project.task",
        copy=False,
    )

    @api.model_create_multi
    def create(self, list_value):
        projects = super(ProjectProject, self).create(list_value)
        projects.helpdesk_task_create()
        return projects

    def helpdesk_task_create(self):
        Task = self.env["project.task"]
        for project in self:
            if not project.helpdesk_task_id:
                task_id = Task.create(
                    {
                        "project_id": project.id,
                        "name": "HelpDesk",
                    }
                )
                project.helpdesk_task_id = task_id
