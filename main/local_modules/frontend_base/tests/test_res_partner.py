# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
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
import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.partner_pool.__dryRun__ = True
        self.country_pool = self.env['res.country']
        self.canada = self.country_pool.browse(39)

    def test_small_image_url_exists(self):
        """Check if the field exist on res.partner."""
        partner = self.partner_pool.create({
            'name': 'tpartner',
            'small_image_url': 'tsmall_image_url',
        })
        self.assertEqual(partner.small_image_url, 'tsmall_image_url')

    def test_write_resetSmallImageUrl(self):
        """Check if the field small_image_url is reset when image is set."""
        partner = self.partner_pool.create({
            'name': 'tpartner',
            'small_image_url': 'tsmall_image_url',
        })
        self.assertEqual(partner.small_image_url, 'tsmall_image_url')
        partner.write({'image': False})
        self.assertEqual(partner.small_image_url, False)

    def test_location_return(self):
        """Check the return of the method with city, state and country."""
        self.assertEqual(
            'Montréal, Québec, Canada',
            self.partner_pool.get_location(
                city='Montréal', state='Québec', country='Canada'
            )
        )

    def test_location_returnNoCity(self):
        """Check the return of the method with state, country and no city."""
        self.assertEqual(
            'Québec, Canada',
            self.partner_pool.get_location(state='Québec', country='Canada')
        )

    def test_location_returnNoState(self):
        """Check the return of the method with city, country and no state."""
        self.assertEqual(
            'Montréal, Canada',
            self.partner_pool.get_location(city='Montréal', country='Canada')
        )

    def test_location_returnNoCountry(self):
        """Check the return of the method with city, state and no country."""
        self.assertEqual(
            'Montréal, Québec',
            self.partner_pool.get_location(city='Montréal', state='Québec')
        )

    def test_infoWindowDetails_return(self):
        """Check the template the method returns."""
        partner = self.partner_pool.create({
            'name': 'tpartner',
            'small_image_url': 'tsmall_image_url',
            'street': '8017 Avenue Chateaubriand',
            'zip': 'H2R 2M7',
            'city': 'Montreal',
            'country_id': self.canada.id,
            'website': 'http://www.cgstudiomap.org',
            'industry_ids': [(6, 0, [1, 2])]
        })
        res = (
            '<div id="iw-container">'
            '<div class="iw-title">'
            '<a href="{0.partner_url}">tpartner</a>'
            '</div>'
            '<div class="iw-content">'
            '<p>Montreal, Canada</p>'
            '<a itemprop="name" href="?company_status=open&search=Animation">'
            '<span class="label label-info">Animation</span>'
            '</a> '
            '<a itemprop="name" href="?company_status=open&search=Advertising">'
            '<span class="label label-info">Advertising</span></a>'
            '</div>'
            '<div id="map_info_footer"><a href="{0.partner_url}">'
            'More ...</a></div></div>'.format(partner)
        )
        self.assertEqual(
            partner.info_window_details(
                partner.id,
                partner.name,
                [i.name for i in partner.industry_ids],
                'open',
                partner.city,
                partner.state_id.name,
                partner.country_id.name
            ),
            res
        )

    def test_linkToStudioPage_returnValue(self):
        """check the value returned by the method link_to_studio_page."""
        self.assertEqual(
            '<a href="http://www.example.com">tname</a>',
            self.partner_pool.link_to_studio_page('http://www.example.com', 'tname')
        )