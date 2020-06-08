# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'mcm academy website theme',
    'version' : '1.1',
    'summary': 'Website',
    'sequence': 15,
    'description': """
add css and js files to website model
    """,
    'category': 'website',
    'website': 'https://www.odoo.com/page/billing',
    # 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['web','website','website_sale','sale','payment'],
    'data': [
        'views/ressources.xml',
        'views/template.xml',
        'views/templates.xml',
        'views/product_public_category.xml',
        'views/payment_acquirer.xml',
        'views/formation_taxi.xml',
        'views/formation_vmdtr.xml',
        'views/formation_vtc.xml',
        'views/website_sale.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
