# -*- coding: utf-8 -*-
{
    'name': "Timesheets User",

    'summary': "Track employee time on tasks",

    'description': "Track employee time on tasks",

    'author': "Dimension3",
    'contributors': ["Juan Arcos juanparmer@gmail.com"],
    'website': "www.d-3.com.au",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Timesheets',
    'version': '17.0.1.1',

    # any module necessary for this one to work correctly
    'depends': [
        'timesheet'
        # 'timesheet_grid'
    ],

    # always loaded
    'data': [
        'data/ir_cron_data.xml',
        'data/mail_message_data.xml',
        'data/mail_template_data.xml',
        'data/product_product_data.xml',
        'security/ir.model.access.csv',
        'report/report_timesheet_templates.xml',
        'views/mail_mail_views.xml',
        'views/project_project_views.xml',
        'wizard/res_config_view.xml',
        'wizard/timesheet_weekly_views.xml',
        'wizard/external_api_views.xml',
    ],

    # license
    'license': 'LGPL-3'
}

