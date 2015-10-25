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
    'name': 'Portal User',
    'version': '256',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Settings of portal user',
    'depends': [
        'account',
        'portal',
        'portal_sale',
        'website_partner',
        'website_menu_by_user_status',
        'res_partner_industry',
        'web_m2x_options',
        'crm',
        'res_partner_missing_details',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'views/portal_items.xml',
        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/website_menu.xml',
        'security/ir.model.access.csv',
        'security/base_security.xml',
    ],
    'installable': True,
}
