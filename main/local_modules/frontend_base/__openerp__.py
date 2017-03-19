# -*- encoding: utf-8 -*-
{
    'name': 'Frontend Base',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Web',
    'summary': 'Base for frontend pages.',
    'depends': [
        'website',
        'res_group_archetype',
        'res_partner_industry',
    ],
    'data': [
        'templates/template_body.xml',
        'templates/template_engine.xml',
        'templates/template_head.xml',
        'templates/template_html.xml',
    ],
    'installable': True,
}
