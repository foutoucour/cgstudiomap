# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
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
    'name': 'Main For res.partner Based Modules',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Main module that will install res.partner based modules.',
    'description': """
Main Module
===========
This module contains the dependencies to install all res.partner based modules.

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>

""",
    'depends': [
        'res_partner_email_validation',
        'res_partner_filter',
        'res_partner_industry',
        'res_partner_location_validation',
        'res_partner_missing_details',
        'res_partner_filter',
        'res_partner_social_networks',
        'res_partner_url_validation',
        'res_partner_moderator_supervision',
        'res_partner_count',
        # partner-contact
        'partner_relations',
    ],
    'data': [],
    'installable': True,
    'application': True,
}
