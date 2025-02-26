# -*- coding: utf-8 -*-
{
    'name': "Statement User",

    'summary': "Account Customer Statements",

    'description': """
Long description of module's purpose
    """,

    'author': "D-3system",
    'website': "https://www.d-3system.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Localizations/Reporting',
    'version': '17.1',

    # any module necessary for this one to work correctly
    'depends': ['l10n_account_customer_statements'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],

    # License
    'license': 'LGPL-3',
}

