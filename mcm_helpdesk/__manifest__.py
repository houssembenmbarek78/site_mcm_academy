# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MCM Helpdesk',
    'description': " personaliser helpdesk ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Helpdesk',
    'sequence': 15,
    'summary': 'Helpdesk',
    'depends': [
        'website_helpdesk',
        'helpdesk',
        'web_enterprise'
    ],
    'description': "Rajout de la champ ville(s) à la vue article",
    'data': [
        # 'views/helpdesk_team.xml',
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