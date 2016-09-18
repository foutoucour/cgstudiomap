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
    'name': 'Frontend Studio',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Web',
    'summary': 'Module that build the page that manage studio.',
    'depends': [
        'website',
        'frontend_base',
        'frontend_listing',  # url of the map page.
        'main_data',  # for state
        'res_partner_location_validation',
        'res_partner_social_networks',
        'res_partner_relations_viewed',
    ],
    'data': [
        'templates/template_body.xml',
        'templates/template_body_edit_mode.xml',
        'templates/template_engine.xml',
        'views/website_views.xml',
    ],
    'installable': True,
}
