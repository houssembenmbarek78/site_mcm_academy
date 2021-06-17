# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Crm marketing automation',
    'summary': """
        Crm integration""",
    'version': '1.0',
    'license': 'AGPL-3',
    'category': 'API',
    'author': 'MCM ACADEMY',
    'website': '',
    'depends': ['base','crm','sale'
    ],
    'data': [
      'views/crm_lead.xml',
      'data/ir_cron.xml',
    ],
    'demo': [
    ],
    'development_status': '',
    'application': False,
    'installable': True,
}
