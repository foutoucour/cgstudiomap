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


class TestResPartnerDomains(common.TransactionCase):
    """Test suites for domain scopes."""
    def setUp(self):
        super(TestResPartnerDomains, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.partner_pool.__dryRun__ = True
        self.country_pool = self.env['res.country']
        self.usa = self.country_pool.browse(235)
        self.india = self.country_pool.browse(105)

    def test_whenIndiaIsSearched_thenOnlyStudioInIndiaAreReturned(self):
        """
        Given the studio A is in the country India
        Given the studio B is in the city indianapolis, USA
        When India is searched
        Then only the studio A is returned

        :related ticket:
        * https://github.com/cgstudiomap/cgstudiomap/issues/700
        """
        self.partner_pool.create({
            'name': 'Studio A',
            'is_company': True,
            'street': 'DLF Cyber City',
            'zip': '122002',
            'city': 'Gurgaon',
            'country_id': self.india.id,
            'website': 'http://www.cgstudiomap.org',
        })
        self.partner_pool.create({
            'name': 'Studio B',
            'is_company': True,
            'street': '6345 Carrollton Avenue',
            'zip': '46220',
            'city': 'Indianapolis',
            'country_id': self.usa.id,
            'website': 'http://www.cgstudiomap.org',
        })
        search_domain = self.partner_pool.get_company_domain('India')
        result = self.partner_pool.search(search_domain.search, order=search_domain.order, limit=search_domain.limit)
        self.assertTrue(result, msg='The search India should have at least one result.')
        # use all() here, as we might have some partners for other tests that are infect the test
        # unfortunately. Anyway the fix aims to remove any result that looks like the need.
        self.assertTrue(
            all(partner.country_id == self.india for partner in result),
            msg="{0} is/are not in India and should have been excluded form the search.".format(
                [partner.name for partner in result if partner.country_id != self.india]
            )
        )

    def test_whenAStudioNameMatchsThesearch_ThenTheStudioIsReturned(self):
        """
        Given a studio is named "Toto Tata"
        When To is searched
        Then the studio is found
        """
        name = 'Toto Tata'
        self.partner_pool.create({
            'name': name,
            'is_company': True,
            'street': '110 Greene Street',
            'zip': '10012',
            'city': 'New York',
            'country_id': self.usa.id,
            'website': 'http://www.cgstudiomap.org',
        })
        # first part of the name
        search_term = 'Toto'
        search_domain = self.partner_pool.get_company_domain(search_term)
        result = self.partner_pool.search(search_domain.search, order=search_domain.order, limit=search_domain.limit)
        # Make sure there is at least a result
        self.assertTrue(result, msg='The search {0} should have at least one result.'.format(search_term))
        # use all() here, as we might have some partners for other tests that are infect the test
        # unfortunately. Anyway the fix aims to remove any result that looks like the need.
        self.assertTrue(
            all(search_term in partner.name  for partner in result),
            msg="{0} is/are not named with {1} and should have been excluded form the search.".format(
                [partner.name for partner in result if search_term not in partner.name], search_term
            )
        )

        # second part of the name
        # to be sure the engine understands all
        search_term = 'Tata'
        search_domain = self.partner_pool.get_company_domain(search_term)
        result = self.partner_pool.search(search_domain.search, order=search_domain.order, limit=search_domain.limit)
        # Make sure there is at least a result
        self.assertTrue(result, msg='The search {0} should have at least one result.'.format(search_term))
        # use all() here, as we might have some partners for other tests that are infect the test
        # unfortunately. Anyway the fix aims to remove any result that looks like the need.
        self.assertTrue(
            all(search_term in partner.name  for partner in result),
            msg="{0} is/are not named with {1} and should have been excluded form the search.".format(
                [partner.name for partner in result if search_term not in partner.name], search_term
            )
        )

    def test_whenNewYorkIsSearched_thenStudiosInNewYorkCityAreFound(self):
        """
        Given a Studio NY is in the city New York
        When New York is searched
        Then the studio NY is found.
        """
        new_york = 'New York'
        self.partner_pool.create({
            'name': 'Studio NY',
            'is_company': True,
            'street': '110 Greene Street',
            'zip': '10012',
            'city': new_york,
            'country_id': self.usa.id,
            'website': 'http://www.cgstudiomap.org',
        })
        search_domain = self.partner_pool.get_company_domain(new_york)
        result = self.partner_pool.search(search_domain.search, order=search_domain.order, limit=search_domain.limit)
        # Make sure there is at least a result
        self.assertTrue(result, msg='The search {0} should have at least one result.'.format(new_york))
        # use all() here, as we might have some partners for other tests that are infect the test
        # unfortunately. Anyway the fix aims to remove any result that looks like the need.
        self.assertTrue(
            all(partner.city == new_york for partner in result),
            msg="{0} is/are not in {1} and should have been excluded form the search.".format(
                [partner.name for partner in result if partner.city != new_york], new_york
            )
        )
