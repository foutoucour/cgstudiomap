# -*- encoding: utf-8 -*-

{
    'name': 'Res Partner Locate Me Stats',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Allows to keep a track of who used the Locate Me feature.',
    'depends': [
    ],
    'external_dependencies': {
    },
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_locate_me_stats_view.xml',
    ],
    'installable': True,
}
