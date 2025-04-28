# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import fields, models

current_format = '%d/%m/%Y'
desired_format = '%Y-%m-%d'


class ForecastReport(models.TransientModel):
    _name = 'forecast.report'
    _description = 'Forecast Report'

    #

    date_start = fields.Date(string='Start date')
    date_end = fields.Date(string='End date')

    product_id = fields.Many2one('product.product')
    products_ids = fields.Many2many('product.product')
    product_tmpl_id = fields.Many2one('product.template')

    def action_confirm(self):
        Product = self.env['forecast.report.product'].sudo()

        Product.search([('user_id', '=', self.env.user.id)]).unlink()

        return self.product_tmpl_id.action_product_tmpl_forecast_report()

        self.action_product()

        action = self.env.ref('forecast_report.forecast_report_product_action')
        action = self.env["ir.actions.actions"]._for_xml_id('stock.stock_forecasted_product_template_action')

        return action

    def action_product(self):
        Forecasted = self.env['stock.forecasted_product_product'].sudo()
        Product = self.env['forecast.report.product'].sudo()
        Template = self.env['product.product']

        products_ids = self.products_ids
        if not products_ids:
            products_ids = Template.search([('type','=','product')])

        values = Forecasted.get_report_values(docids=products_ids.ids)
        docs = values.get('docs')
        lines = docs.get('lines')

        def strptime(date_string, obj=False):
            date_object = datetime.strptime(date_string, current_format)
            formatted_date = date_object.strftime(desired_format)
            if obj:
                return date_object
            return formatted_date

        for line in lines:
            document_in = line.get('document_id')
            document_out = line.get('document_out')
            receipt_date = line.get('receipt_date')
            delivery_date = line.get('delivery_date')
            product = line.get('product')
            quantity = line.get('quantity')
            move_out = line.get('move_out')
            move_in = line.get('move_in')

            date = receipt_date or delivery_date
            if not date:
                continue
            
            date_obj = fields.Date.to_date(strptime(date, obj=True))
            if date_obj < self.date_start or date_obj > self.date_end:
                continue

            vals = {
                'user_id': self.env.user.id,
                'document_in': document_in and document_in.get('name') or '',
                'document_out': document_out and document_out.get('name') or '',
                'receipt_date': receipt_date and strptime(receipt_date) or False,
                'delivery_date': delivery_date and strptime(delivery_date) or False,
                'move_out': move_out and move_out.get('name') or '',
                'move_in': move_in and move_in.get('name') or '',
                'product_id': product.get('id'),
                'product_qty': quantity,
                'date': strptime(date),
            }

            Product.create(vals)


class ForecastReportProduct(models.TransientModel):
    _name = 'forecast.report.product'
    _description = 'Forecast Product'

    date = fields.Date()

    delivery_date = fields.Date()

    document_in = fields.Char()
    document_out = fields.Char()

    move_in = fields.Char()
    move_out = fields.Char()

    product_id = fields.Many2one('product.product')
    product_qty = fields.Float()
    product_tmpl_id = fields.Many2one('product.template')

    receipt_date = fields.Date()

    user_id = fields.Many2one('res.users')
