# -*- coding: utf-8 -*-

import requests
import json

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    zoominfo_id = fields.Char()
    zoominfo_type = fields.Selection([
        ('contact', 'Contact'),
        ('company', 'Company'),
    ])

    def action_zoominfo(self):
        jwt = self.env.company_id.zoominfo_authenticate()
        return True
