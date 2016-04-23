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

from openerp.exceptions import ValidationError
from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites for social network fields added in res.partner."""

    def setUp(self):
        """Overcharge the default setUp to expose the partner_pool."""
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

        self.twitter_url = 'https://twitter.com/cgstudiomap'
        self.youtube_url = 'https://www.youtube.com/mpcvfx'
        self.vimeo_url = 'https://vimeo.com/mpcvfx'
        self.linkedin_url = 'https://www.linkedin.com/company/cgstudiomap-com'
        self.linkedin_url_user = 'https://ca.linkedin.com/in/jordirieracg'
        self.facebook_url = 'https://www.facebook.com/Moving.Picture.Company/'
        self.wikipedia_url = 'https://en.wikipedia.org/wiki/Sony_Pictures_Imageworks'
        self.partner = self.partner_pool.create({'name': 'tname'})

    def test_twitter_constrains(self):
        """Check if we can add value to the twitter field."""
        partner = self.partner_pool.create(
            {'name': 'tname', 'twitter': self.twitter_url}
        )
        self.assertEqual(partner.twitter, self.twitter_url)

    def test_twitter_value(self):
        """Test the method _validate_twitter_url raise Error if the
        given value is not a valid twitter url.
        """
        with self.assertRaises(ValidationError):
            self.partner._validate_twitter_url(
                'https://twitter.ca/cgstudiomap'
            )

    def test_youtube_constrains(self):
        """Check if we can add value to the youtube field."""
        partner = self.partner_pool.create(
            {'name': 'tname', 'youtube': self.youtube_url}
        )
        self.assertEqual(partner.youtube, self.youtube_url)

    def test_youtube_value(self):
        """Test the method _validate_youtube_url raise Error if the
        given value is not a valid youtube url.
        """
        with self.assertRaises(ValidationError):
            self.partner._validate_youtube_url(
                'https://www.youtube.ca/mpcvfx'
            )

    def test_vimeo_constrains(self):
        """Check if we can add value to the vimeo field."""
        partner = self.partner_pool.create(
            {'name': 'tname', 'vimeo': self.vimeo_url}
        )
        self.assertEqual(partner.vimeo, self.vimeo_url)

    def test_vimeo_value(self):
        """Test the method _validate_vimeo_url raise Error if the
        given value is not a valid vimeo url.
        """
        with self.assertRaises(ValidationError):
            self.partner._validate_vimeo_url(
                'https://www.vimeo.ca/mpcvfx'
            )

    def test_linkedin_constrains(self):
        """Check if we can add value to the linkedin field."""
        partner = self.partner_pool.create(
            {'name': 'tname', 'linkedin': self.linkedin_url}
        )
        self.assertEqual(partner.linkedin, self.linkedin_url)
        partner_user = self.partner_pool.create(
            {'name': 'tname', 'linkedin': self.linkedin_url_user}
        )
        self.assertEqual(partner_user.linkedin, self.linkedin_url_user)

    def test_linkedin_value(self):
        """Test the method _validate_linkedin_url raise Error if the
        given value is not a valid linkedin url.

        Case /company/ is missing.
        """
        with self.assertRaises(ValidationError):
            self.partner._validate_linkedin_url(
                'https://www.linkedin.com/mpcvfx'
            )

    def test_facebook_constrains(self):
        """Check if we can add value to the facebook field."""
        partner = self.partner_pool.create(
            {'name': 'tname', 'facebook': self.facebook_url}
        )
        self.assertEqual(partner.facebook, self.facebook_url)

    def test_facebook_value(self):
        """Test the method _validate_facebook_url raise Error if the
        given value is not a valid facebook url.
        """
        with self.assertRaises(ValidationError):
            self.partner._validate_facebook_url(
                'https://www.facebook.ca/mpcvfx'
            )
