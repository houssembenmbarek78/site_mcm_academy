# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'facture acompte',
    'description': " Créer une facture d'acompte  ",
    'author': "Houssem - modified by Seifeddinne",
    'maintainer': 'DIGIMOOV',
    'category': 'account',
    'sequence': 15,
    'summary': 'account',
    'depends': [
        'base',
        'account',
        'mcm_add_fields',
        'mcm_session',
    ],
    'description': " Créer une facture d'acompte  ",
    'data': [
        'views/account.xml',
        'views/account_acompte_wizard.xml',
        'security/ir.model.access.csv',
        'views/other_info_inherit_view.xml',
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