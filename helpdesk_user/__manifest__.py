# -*- coding: utf-8 -*-
{
    'name': "Helpdesk",

    'summary': "Services/Helpdesk",

    'description': "",

    'author': 'Dimension3',
    'contributors': ['Juan Arcos juanparmer@gmail.com'],
    'website': 'https://sys.d-3system.com.au',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Helpdesk',
    'version': '17.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk_timesheet'],

    # always loaded
    'data': [
        'data/ir_cron_data.xml',
        'view/helpdesk_ticket_view.xml'
    ],

    # license
    'license': 'OEEL-1',
}
