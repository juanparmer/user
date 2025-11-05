# -*- coding: utf-8 -*-
{
    'name': "Project User",

    'summary': "Bridge module for project and user",

    'description': """
        Add changes on task view
    """,

    'author': "D-3system",
    'contributors': ["Juan Arcos juanparmer@gmail.com"],
    'website': "https://www.d-3system.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Project',
    'version': '19.0.1.1.1',

    # any module necessary for this one to work correctly
    'depends': ['project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'view/project_task_views.xml',
        'wizard/project_task_wizard.xml',
    ],

    # "assets": {
    #     "web.assets_backend": [
    #         'project_user/static/src/components/**/*',
    #     ],
    #     'project.webclient': [
    #         'project_user/static/src/components/project_task_state_selection/*',
    #     ],
    # },

    # License
    'license': 'LGPL-3',
}
