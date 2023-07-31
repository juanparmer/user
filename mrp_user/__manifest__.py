# -*- coding: utf-8 -*-
{
    'name': "Manufacturing User",

    'summary': "Manufacturing Orders & BOMs",

    'description': "Manufacturing Orders & BOMs",

    'author': "Odone",
    'website': "https://www.odone.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing/Manufacturing',
    'version': '15.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp_landed_costs'],

    # always loaded
    'data': [
        'security/res_groups_security.xml',
        'security/ir.model.access.csv',
        'data/account_journal_data.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/stock_landed_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/product_product_demo.xml',
    ],
    # license
    'license': 'LGPL-3',
}
