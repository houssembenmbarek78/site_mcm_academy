# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Exam',
    'description': "Ce module permet d'ajouter une interface qui comporte toutes les informations des examens "
                   "pour chaque client telque notes QCM & QRO. Ce module nous permet aussi d'effectuer les impressions "
                   "des fichiers sous forme des PDF telque les convocations et les relevées de notes. "
                   "Ce module permet d'ajouter un champ signature dans l'interface de la société dans odoo,"
                   "Et aussi la génération des PDF des relevées de notes en masse",
    'author': "Houssem BEN MBAREK & Takwa MEJRI",
    'maintainer': 'DIGIMOOV',
    'website': "https://www.digimoov.fr/",
    'category': 'Partner',
    'sequence': 15,
    'summary': 'This module for print pdf as convocation, relevé de note, '
               'from contact view, also Import all Exam-informations as note (QCM, QRO)',
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
        'report/menu.xml',
        'report/generate_releve_de_notes.xml',
        'report/convocation_contact.xml',
        'report/print_releve_note_mass.xml',
        'report/mass_pdf_relevé_de_note_examen.xml',
        'report/attestation_suivi_formation.xml',
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
