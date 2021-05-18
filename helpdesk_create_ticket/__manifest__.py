# Copyright 2018 Pierre Faniel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Helpdesk fetch mail',
    'category': 'Website',
    'summary': 'Helpdesk fetch mail',
    'version': '1.0.0',
    'license': 'AGPL-3',
    'sequence': '60',
    'description': '''
        block create new partner when fetching mail and create ticket
    ''',
    'author': 'Digimoov',
    'depends': [
        'base',
        'helpdesk'
    ],
    'data': [
        'data/scheduled_unlink_tickets.xml'
    ],
    'images': [
    ],
    'installable': True,
    'application': False,
}
