# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MCM Helpdesk',
    'description': " Personaliser helpdesk ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Helpdesk',
    'sequence': 15,
    'summary': 'Helpdesk',
    'depends': [
        'website_helpdesk',
        'helpdesk',
    ],
    'description': "Personaliser helpdesk",
    'data': [
        'views/helpdesk_template.xml',
        'views/helpdesk_team.xml',
    ],
    'qweb': [],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}