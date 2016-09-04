# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Main Data Module',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Main Module, that install data, views etc.',
    'depends': [
        'crm',
        'website',
        'website_blog',
        'website_crm',
        'crm_partner_assign',
        'base_geolocalize',
        'geoengine_partner',
        'base_geoengine',
        'geoengine_base_geolocalize',
        'auth_signup',
        'web_tree_image',
        'web_widget_text_markdown',
        'res_group_archetype',
    ],
    'data': [
        'data/company_details.xml',
        'data/res_groups_data.xml',
        'data/res_users_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'views/website_blog_view.xml',
        'views/res_partner_view.xml',
        'views/geo_partner_view.xml',
        'views/base_partner_merge_view.xml',
        'templates/web_layout.xml',
    ],
    'installable': True,
}
