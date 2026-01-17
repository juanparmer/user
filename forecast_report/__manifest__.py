# -*- coding: utf-8 -*-
{
    'name': "Forecast Report",

    'summary': "Forecast Report",

    'description': """
        Forecast Report
    """,

    'author': "D3System",
    'website': "https://www.d-3system.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '17.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/forecast_report_view.xml',
    ],
    # License
    'license': 'LGPL-3',
}
