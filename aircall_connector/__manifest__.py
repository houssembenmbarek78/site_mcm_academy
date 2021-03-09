# -*- coding: utf-8 -*-
{
    'name': "Aircall Connector",

    'summary': """Aircall Odoo Connector""",

    'description': """
        Aircall Odoo Connector
    """,

    'author': "Wajahat Ali",
    'website': "http://www.axiomworld.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.0.3.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/call_history.xml',
        'views/views.xml',
        'views/aircall_setting.xml',
        'wizard/message_wizard.xml',
        'tools/schedulers.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
