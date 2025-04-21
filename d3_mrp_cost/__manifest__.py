# -*- coding: utf-8 -*-
{
    'name': "D3 MRP Cost",

    'summary': "MRP Cost",

    'description': """
        Creates accounting entries for the additional operation costs in manufacturing orders.
    """,

    'author': "d-3systems",
    'website': "https://d-3system.com.au/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing/Manufacturing',
    'version': '17.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp_account'],

    # always loaded
    'data': [
        'views/res_config_views.xml',
    ],

    # license
    'license': 'LGPL-3',
}

