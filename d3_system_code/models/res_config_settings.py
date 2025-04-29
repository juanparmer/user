from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_d3_mrp_cost = fields.Boolean()
    module_d3_product_image = fields.Boolean()
    module_d3_website_price = fields.Boolean()
    module_d3_wesbite_rebranding = fields.Boolean()
    module_helpdesk_user = fields.Boolean()
    module_project_user = fields.Boolean()
    module_timesheet_user = fields.Boolean()
    module_d3_customer_statement = fields.Boolean()