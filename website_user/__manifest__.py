# -*- coding: utf-8 -*-
{
    'name': "User Website",

    'summary': "Change the brand promotion message",

    'description': """  """,

    'author': "Dimension3 System",
    'website': "https://d-3system.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'contributors': ["Juan Arcos juanparmer@gmail.com"],
    'version': '19.1',

    # any module necessary for this one to work correctly
    'depends': ['website'],

    # always loaded
    'data': [
        'data/ir_cron_data.xml',
        'templates/web_template.xml',
        'templates/website_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # license
    'license': 'LGPL-3'
}

