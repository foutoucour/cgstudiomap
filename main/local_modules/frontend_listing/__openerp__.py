# -*- encoding: utf-8 -*-

{
    'name': 'Frontend Listing',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Web',
    'summary': 'Module that build the page that list companies.',
    'depends': [
        'web',
        'website',
        'crm_partner_assign',
        'frontend_base',
        'res_group_archetype',
        'website_menu_by_user_status',
    ],
    'data': [
        'templates/template_body.xml',
        'templates/template_engine.xml',
        'data/website_menus.xml',
    ],
    'installable': True,
}
