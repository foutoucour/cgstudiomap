# -*- coding: utf-8 -*-
import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartnerLocation(common.TransactionCase):
    """Test Suite for the methods that set location for the partner."""

    def setUp(self):
        """Build the partners for each tests."""
        super(TestResPartnerLocation, self).setUp()

        self.partner_pool = self.env['res.partner']
        # to avoid to have google checks to be triggered.
        self.partner_pool.__dryRun__ = True
        self.values = {
            'name': 'tname',
            'is_company': True,
            'street': '8017 Avenue Chateaubriand',
            'zip': 'H2R 2M7',
            'city': 'Montreal',
            'country_id': 39,  # Canada
            'website': 'http://www.cgstudiomap.org',
        }

    def test_full_location_returnValue(self):
        """Check the return value for given partner.

        Need to be sure the zip code is here.
        See https://github.com/cgstudiomap/cgstudiomap/issues/671
        """
        partner = self.partner_pool.create(self.values)
        self.assertEqual(
            partner.full_location, '8017 Avenue Chateaubriand, Montreal, H2R 2M7'
        )
