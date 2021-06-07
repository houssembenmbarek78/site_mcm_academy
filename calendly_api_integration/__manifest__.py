# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Calendly',
    'summary': """
        Calendly api integration""",
    'version': '1.0',
    'license': 'AGPL-3',
    'category': 'API',
    'author': 'MCM ACADEMY',
    'website': '',
    'depends': ['base','mcm_session','crm','website','mcm_website_theme','partner_exam'
    ],
    'data': [
        'data/api_data.xml',
        'views/partner.xml',
        'views/menu.xml',
        'views/calendly.xml',
        # 'views/lead.xml',
    ],
    'demo': [
    ],
    'development_status': '',
    'application': False,
    'installable': True,
}
