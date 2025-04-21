# -*- coding: utf-8 -*-
{
    'name': "D3 Product Image",

    'summary': "Product Image",

    'description': """
        This module extends Odoo's Sales Management by displaying product images in the PDF sales report and on the customer portal.
    """,

    'author': "d-3systems",
    'website': "https://d-3system.com.au/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '17.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates/sale_order_templates.xml',
        'views/res_config_views.xml',
    ],
    # license
    'license': 'LGPL-3',
}

