# -*- coding: utf-8 -*-
{
    'name': "plateforme_pedagogique",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "DIGIMOOV",
    'website': "https://www.digimoov.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'mcm_session',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/groupe_plateforme.xml',
        'views/partner.xml',
        'views/gerer_user_ir_cron.xml',
        'views/get_parcours_ir_cron.xml',
        'views/parcours.xml',
        'views/session.xml',
        'views/users_stats.xml',

    ],
}
