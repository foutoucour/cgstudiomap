# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
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
    'name': 'Main Module',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Main Module, that install everything',
    'description': """
Main Module
===========
This module contains the dependencies to install all others modules

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>

""",
    # Don't add demo module here as it should not be installed on prod server.
    'depends': [
        # odoo
        'product',
        'sale',
        'website_crm',
        'website_blog',
        'auth_signup',
        # telephony
        'base_phone_validation',
        # web
        'web_tree_image',
        'web_widget_text_markdown',
        'web_m2x_options',
        # odoo_sentry
        'odoo_sentry',
        # server-tools
        'auditlog',
        'disable_openerp_online',
        'admin_technical_features',
        # geoengine
        'geoengine_base_geolocalize',
        # Applications
        'res_partner',
        'frontend',
        # website
        'portal_user',
        'main_data',
        'shared_web_theme',
        'website_blog_group_published_only',
        'res_group_archetype',
    ],
    'data': [],
    'installable': True,
    'application': True,
}
