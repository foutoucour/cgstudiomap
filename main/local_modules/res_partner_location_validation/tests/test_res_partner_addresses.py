# -*- coding: utf-8 -*-
"""
Test suite that check when a partner is created with a given address
we have the expected behaviour.
"""
import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites for addresses that causes issues on cgstudiomap."""

    def setUp(self):
        """Overcharge the default setUp to expose the partner_pool."""
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.country_state = self.env['res.country.state']
        self.country = self.env['res.country']

    def test_issue791(self):
        """
        Given there is already a state with a close name
        When another state is created
        Then the correct state is registered

        See: https://github.com/cgstudiomap/cgstudiomap/issues/791
        """
        # Set up a state with a really close name that reveal the bug
        self.country_state.create({
            'name': 'Comunidad Valenciana', 'code': 'Com', 'country_id': 69,  # spain
        })

        self.__test_create({
            'street': '11 Calle de Genova',
            'city': 'Madrid',
            'zip': '28004',
            'country_id': 76,
            'country_name': 'Spain',
            'street2': '',
            'name': 'Home Sweet Home',
            'state_id': False,
            'state_name': 'Comunidad de Madrid',
        })

    def test_france(self):
        """Test a create for a partner in France."""
        self.__test_create({
            'street': '64 Cours Victor Hugo',
            'city': 'Bordeaux',
            'zip': '33000',
            'country_id': 76,
            'country_name': 'France',
            'street2': '',
            'name': 'Home Sweet Home',
            'state_id': False,
            'state_name': 'Nouvelle-Aquitaine',
        })

    def test_canada(self):
        """test a create for a partner in canada."""
        self.__test_create({
            'street': '1605 Richards Street',
            'city': 'Vancouver',
            'zip': 'V6Z',
            'country_id': 39,
            'country_name': 'Canada',
            'street2': '',
            'name': 'Home Sweet Home',
            'state_id': False,
            'state_name': 'British Columbia',
        })

    def test_issue763(self):
        """City that is set to England instead of Brentford

        See: https://github.com/cgstudiomap/cgstudiomap/issues/763
        """
        self.__test_create({
            'street': '1110 Great West Road',
            'city': 'Brentford',
            'zip': 'TW8 0GP',
            'country_id': 233,
            'country_name': 'United Kingdom',
            'street2': 'Qwest suite 1.05',
            'name': '3dmd',
            'state_id': False,
            'state_name': 'England',
        })

    def __test_create(self, create_vals):
        """Generic tests to check the values set for location during a create."""
        partner = self.partner_pool.create(create_vals)
        self.assertEqual(create_vals['city'], partner.city)
        self.assertEqual(create_vals['street'], partner.street)
        self.assertEqual(create_vals['zip'], partner.zip)
        self.assertEqual(create_vals['country_name'], partner.country_id.name)
        self.assertEqual(create_vals['name'], partner.name)
        self.assertEqual(create_vals['state_name'], partner.state_id.name)
