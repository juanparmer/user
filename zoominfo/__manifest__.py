# -*- coding: utf-8 -*-
{
    'name': "API Zoominfo",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],

    # always loaded
    'data': [
        'data/ir_cron_data.xml',
        'views/crm_lead_view.xml',
        'views/res_config_view.xml',
    ],
    # License
    'license': 'LGPL-3',
}
