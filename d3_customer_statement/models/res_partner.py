# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_statement = fields.Boolean(string="Send Statement?", default=False)

    def send_customer_statement(self):
        template = self.env.ref("d3_customer_statement.mail_customer_statement")
        domain = [
            ("customer_statement", "=", True),
            ("parent_id", "=", False),
            ("total_due", ">", 0.0)
        ]
        partners = self.search(domain)
        if not partners:
            return False
        template.send_mail_batch(partners.ids)
        return True

    def prepare_customer_statement(self):
        options = None

        date = fields.Date.today().replace(day=1)
        date_to = fields.Date.subtract(date, days=1)
        date_from = date_to.replace(day=1)
        report = self.env.ref("account_reports.partner_ledger_report")
        options = {
            "date": {"date_from": date_from, "date_to": date_to},
            "unreconciled": False,
            "report_id": report.id,
        }

        vals = self._prepare_customer_statement_values(options=options)
        vals.update(company=self.company_id or self.env.company)

        return vals
