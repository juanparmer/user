# -*- coding: utf-8 -*-
{
    'name': "Project User",

    'summary': "Bridge module for project and user",

    'description': """
        Add changes on task view
    """,

    'author': "D-3system",
    'website': "https://www.d-3system.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Project',
    'version': '17.1',

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        'view/project_task_view.xml',
    ],

    # License
    'license': 'LGPL-3',
}
