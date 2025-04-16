# -*- coding: utf-8 -*-

import xmlrpc.client

from odoo import fields, models


class ExternalApiWizard(models.TransientModel):
    _name = "external.api.wizard"
    _description = "External API Wizard"

    date_start = fields.Date(string="Start date", required=True)
    date_end = fields.Date(string="End date", required=True)

    def action_confirm(self):
        company = self.env.company
        
        url = company.api_url
        db = company.api_db
        username = company.api_username
        password = company.api_password

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        uid = common.authenticate(db, username, password, {})

        models.execute_kw(db, uid, password, 'account.analytic.line', 'check_access_rights', ['read'], {'raise_exception': False})
        # _read_group
        # read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True)
        # res_groups = self.env['stock.move.line']._read_group(
        #     [('picking_id', 'in', self.ids), ('product_id', '!=', False), ('result_package_id', '=', False)],
        #     ['picking_id', 'product_id', 'product_uom_id', 'quantity'],
        #     ['__count'],
        # )

        return True
