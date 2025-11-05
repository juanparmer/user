# -*- coding: utf-8 -*-

import xmlrpc.client

from odoo import fields, models


class ExternalApiWizard(models.TransientModel):
    _name = "external.api.wizard"
    _description = "External API Wizard"

    date_start = fields.Date(
        string="Start date",
        required=True,
        default=fields.Date.subtract(fields.Date.today(), days=8),
    )
    date_end = fields.Date(
        string="End date",
        required=True,
        default=fields.Date.subtract(fields.Date.today(), days=2),
    )

    def action_confirm(self):
        company = self.env.company

        url = company.api_url
        db = company.api_db
        username = company.api_username
        password = company.api_password

        if not url:
            return False

        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))
        uid = common.authenticate(db, username, password, {})

        if not uid:
            return False

        domain = [
            ("project_id", "!=", False),
            ("user_id", "=", uid),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
        ]
        fields = ["unit_amount:sum"]
        groupby = ["task_id"]
        lines = models.execute_kw(
            db,
            uid,
            password,
            "account.analytic.line",
            "read_group",
            [domain, fields, groupby],
        )

        if not lines:
            return False

        product = self.env.ref("timesheet_user.product_product_dev")

        invoice_line_ids = []
        for line in lines:
            invoice_line_ids.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "quantity": line.get("unit_amount"),
                        "name": line.get("task_id") and line.get("task_id") [1] or 'Dev',
                        "price_unit": 31.19
                    },
                )
            )
        invoice_vals = {
            "move_type": "out_invoice",
            "invoice_line_ids": invoice_line_ids,
        }
        invoice = self.env["account.move"].create(invoice_vals)
        action = self.env.ref("account.action_move_out_invoice_type").read()[0]
        action.update({"view_mode": "form", "res_id": invoice.id})
        return action
