# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Add states to products',
    'description': " Rajout de la champ ville(s) à la vue article ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Product',
    'sequence': 15,
    'summary': 'Product',
    'depends': [
        'product',
    ],
    'description': "Rajout de la champ ville(s) à la vue article",
    'data': [
        'views/product_template.xml',
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