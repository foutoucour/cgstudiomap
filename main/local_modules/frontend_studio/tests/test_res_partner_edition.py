# -*- coding: utf-8 -*-
import logging

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartnerEdition(common.TransactionCase):
    """Test Suite for the edition of res.partner."""

    def setUp(self):
        """Build the partners for each tests."""
        super(TestResPartnerEdition, self).setUp()

        self.partner_pool = self.env['res.partner']
        # to avoid to have google checks to be triggered.
        self.partner_pool.__dryRun__ = True

    def test_common_values(self):
        """Double check the common values are stable."""
        common_values = self.partner_pool.get_partner_values()
        witness_dict = {
            'id': 0,
            'write_date': '',
            'image_url': '',
            'name': '',
            'website': '',
            'email': '',
            'state': '',
            'street': '',
            'street2': '',
            'city': '',
            'zip': '',
            'industry_ids': [],
            'country_id': 0,
            # social network urls
            'social_networks': {
                'twitter': '',
                'youtube': '',
                'vimeo': '',
                'linkedin': '',
                'facebook': '',
            },
            # phone numbers
            'calls': {
                'phone': '',
                'mobile': '',
                'fax': '',
            }

        }

        self.assertEqual(
            len(common_values), len(witness_dict),
            'The length of the the common values should be the same than the'
            'witness dict.'
        )

        # now checking if the all the keys and values are the same.
        for key, value in witness_dict.iteritems():
            self.assertIn(key, common_values)
            self.assertEqual(value, common_values[key])
