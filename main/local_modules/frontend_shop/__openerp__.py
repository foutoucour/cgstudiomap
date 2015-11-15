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
    'name': 'Frontend Shop',
    'version': '302',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Web',
    'summary': 'Shop Modules',
    'depends': [
        'website',
        'website_menu_by_user_status',
    ],
    'data': [
        # 'templates/template_shop_modules.xml',
        'data/website_menus.xml',
    ],
    'installable': True,
}
