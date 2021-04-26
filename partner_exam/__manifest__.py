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
        'contacts',
        'auto_mass_mailing_marketing',
    ],
    'description': "Rajout note d'examen de condidat ",
    'data': [
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/notes_examens_partner.xml',
        'views/add_signature.xml',
        'report/generation_covocation_en_pdf.xml',
        'report/menu.xml',
        'report/generate_releve_de_notes.xml',
        'report/convocation_contact.xml',
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
