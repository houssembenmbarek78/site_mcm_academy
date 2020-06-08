# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Add fields ',
    'description': " Rajout des champs ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Product',
    'sequence': 15,
    'summary': 'Product',
    'depends': [
        'l10n_fr',
        'account',
        'product',
        'base',
        'contacts'
    ],
    'description': "Rajout des champs",
    'data': [
        'views/product_template.xml',
        'views/res_company.xml',
        'views/res_country_state.xml',
        'views/res_partner.xml',
        'views/res_partner_bank.xml',
        'views/session.xml',
        'report/report_invoice.xml',
        'security/ir.model.access.csv',
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
