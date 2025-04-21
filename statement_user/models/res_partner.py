# -*- coding: utf-8 -*-

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def prepare_customer_statement(self):
        vals = self._prepare_customer_statement_values()
        vals.update(company=self.company_id or self.env.company)
        # Falta, enviarle las fechas del mes anterior
        return vals
