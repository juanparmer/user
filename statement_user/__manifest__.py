# -*- coding: utf-8 -*-
{
    'name': "Statement User",

    'summary': "Account Customer Statements",

    'description': """
Long description of module's purpose
    """,

    'author': "D-3system",
    'contributors': ["Juan Arcos juanparmer@gmail.com"],
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
        'data/ir_cron_data.xml',
        'data/mail_template_data.xml',
        'report/customer_statement_report.xml',
        # 'security/ir.model.access.csv',
        'templates/customer_statement_report.xml',
        'views/res_partner_views.xml',
    ],

    # License
    'license': 'LGPL-3',
}
