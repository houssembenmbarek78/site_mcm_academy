# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Session Ville',
    'description': "",
    'author': "Mejri Takwa",
    'maintainer': 'DIGIMOOV',
    'category': 'Partner',
    'sequence': 15,
    'summary': 'Automatisation des villes dans la session',
    'depends': [
        'base',
        'mcm_session',
        'partner_exam',
        'auto_mass_mailing_marketing',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/session_ville_view.xml',
        'views/adresse_centre_examen.xml',
        'views/inherit_mcmacademy_session.xml',
    ],
    'qweb': [],
    'images': [],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
