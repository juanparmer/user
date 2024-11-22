# -*- coding: utf-8 -*-
{
    'name': "Avansat",

    'summary': "Avansat",

    'description': "Avansat",

    'author': "Odone",
    'contributors': [
        'Juan Arcos juanparmer@gmail.com',
        'Ximena Quijano axquijanog@gmail.com',
    ],
    'website': "https://www.odone.com.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.1',

    # any module necessary for this one to work correctly
    'depends': [
        'account_voucher',
        'base_rest'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/avansat_avansat_views.xml',
        'views/avansat_manifest_views.xml',
        'views/avansat_order_views.xml',
        'views/avansat_wizard_view.xml'
    ],
    
    # license
    'license': "AGPL-3" 
}
