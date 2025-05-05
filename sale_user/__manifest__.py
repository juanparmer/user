# -*- coding: utf-8 -*-
{
    'name': "Sale User",

    'summary': "Extended Sale Module",

    'description': """
        Default Calendar View for Social Scheduling
    """,

    'author': "D3System",
    'website': "https://sys.d-3system.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Sales',
    'version': '18.1',

    # any module necessary for this one to work correctly
    'depends': ['social'],

    # always loaded
    'data': [
        'views/social_post_view.xml',
    ],

    # license
    "license": "LGPL-3",
}

