{
    'name': "plateforme_pedagogique",
    'summary': """
       Gestion des Apprenants sur la plateforme 360Learning""",
    'description': " Ce module permet d'ajouter une interface qui comporte toutes "
                   "les statistiques sur 360 learning pour chaque client. "
                   "Ce module nous permet aussi "
                   "d'ajouter i-Ones automatiquement sur 360 learning, "
                   "de supprimer i-Ones automatiquement après le passage d'examen.",
    'author': "DIGIMOOV, INESS LAHMAR",
    'website': "https://www.digimoov.fr/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base',
                'mail',
                'mcm_session'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/groupe_plateforme.xml',
        'views/partner.xml',
        'views/gerer_user_ir_cron.xml',
        'views/get_parcours_ir_cron.xml',
        'views/parcours.xml',
        'views/session.xml' ,
        'views/users_stats.xml',
    ],
    'application': True,
}
