# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Exam',
    'description': " Rajout note d'examen de condidat  ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Partner',
    'sequence': 15,
    'summary': 'Partner',
    'depends': [
        'base',
        'mcm_session',
    ],
    'description': "Rajout note d'examen de condidat ",
    'data': [
        'views/partner.xml',
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
