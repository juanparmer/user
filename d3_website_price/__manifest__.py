# -*- coding: utf-8 -*-
{
    'name': "d3 Website Price",

    'summary': "Website Price",

    'description': """
        Hide the sale price of specific products in the website interface.
    """,

    'author': "d-3systems",
    'website': "https://d-3system.com.au/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'version': '17.0',

    # any module necessary for this one to work correctly
    'depends': ['website_sale'],

    # always loaded
    'data': [
        'views/website_view.xml',
        'views/product_template_view.xml',
    ],
     # license
    'license': 'LGPL-3',
}

