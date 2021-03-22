# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Documents',
    'description': " App to upload and manage your documents. ",
    'author': "Houssem",
    'maintainer': 'DIGIMOOV',
    'category': 'Contact',
    'sequence': 15,
    'summary': 'Contact',
    'depends': [
        'base',
        'mail',
        'helpdesk',
        'documents',
        'portal',
    ],
    'description': "App to upload and manage your documents.",
    'data': [
        'views/partner_documents.xml',
        'views/documents_document.xml',
        'views/partner_documents_templates.xml',
        'views/res_partner.xml',
        'views/menu.xml',
        # 'views/templates.xml',
        'views/document_template.xml',
        'data/mail_template.xml',
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