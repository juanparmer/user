# -*- coding: utf-8 -*-
{
    'name': " d3 Website Rebranding",

    'summary': "Website Rebranding",

    'description': """

    """,

    'author': "d-3systems",
    'website': "https://d-3system.com.au/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'version': '17.0',

    # any module necessary for this one to work correctly
    'depends': [
        'website_sale'
    ],

    # always loaded
    'data': [
        'data/ir_cron_data.xml',
        'templates/web_template.xml',
        'templates/website_templates.xml',
    ],

    # license
    'license': 'LGPL-3'
}

