# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'mcm academy website portal',
    'version': '1.1',
    'summary': 'Website',
    'sequence': 15,
    'description': """
add css and js files to website model
    """,
    'category': 'website',
    'website': 'https://www.odoo.com/page/billing',
    # 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends': ['base','web', 'website', 'website_sale', 'sale','product','mcm_add_fields','mail','account','mcm_session'],
    'data': [
        'views/sale_portal_templates.xml',
        'views/account_portal_templates.xml',
        'views/res_partner.xml',
        'views/session.xml',
        'views/res_company.xml',
        'views/product_template_details.xml',
        'views/product_template.xml',
        'views/action_formation.xml',
        'views/sale_order_report.xml',
        'views/sale_report.xml',
        'data/mail_data.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
