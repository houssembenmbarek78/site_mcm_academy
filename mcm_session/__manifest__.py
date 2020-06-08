# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Session',
    'description': "module session ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Session',
    'sequence': 15,
    'summary': 'Product',
    'depends': [
        'product',
        'base',
        'fl_auth_signup',
        'account',
        'website_sale',
        'sale',
        'payment',
        'mcm_add_fields',
    ],
    'description': "module session",
    'data': [
        'views/session.xml',
        'views/menu.xml',
        'views/action.xml',
        'views/domain.xml',
        'views/module.xml',
        'views/module_details.xml',
        'views/res_partner.xml',
        'views/stage.xml',
        'views/templates.xml',
        'views/programme.xml',
        'views/message_wizard.xml',
        'views/product_template.xml',
        'views/reports.xml',
        'views/account_move.xml',
        'data/payment_stripe_3X.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
