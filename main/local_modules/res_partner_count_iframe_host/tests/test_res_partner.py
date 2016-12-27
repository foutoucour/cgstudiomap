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
import functools
import logging
import mock
import inspect

import time

from openerp.tests import common

_logger = logging.getLogger(__name__)

def get_module_path(module_name):
    return 'openerp.addons.website_iframe_host.controllers.base.{0}'.format(
        module_name
    )

class TestResPartner(common.TransactionCase):
    """Test suites interaction between partner and res.partner.count.*"""

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.partner1 = self.partner_pool.create({'name': 'partner1'})
        self.partner2 = self.partner_pool.create({'name': 'partner2'})
        self.module_request_path = get_module_path('request')
        self.mock_patch_request = functools.partial(mock.patch, self.module_request_path)

        self.website_iframe_host_pool = self.env['website.iframe.host']

        self.host_name = 'travis.com'
        self.host_url = 'cgstudiomap.{}'.format(self.host_name)
        self.host = self.website_iframe_host_pool.create(
            {'host': self.host_name, 'search_domain': []}
        )
        self.referrer_name = 'travis_referrer.com'
        self.referrer_url = 'http://cgstudiomap.{}'.format(self.referrer_name)
        self.referrer = self.website_iframe_host_pool.create(
            {'host': self.referrer_name, 'search_domain': []}
        )

    def test_whenReferrerIsNotNoneInRequest_thenPartnerHostIsReferrer(self):
        """
        Given a res_partner_count_view is created
        When request referrer is set
        Then the res.partner.count.view stores the name of the referrer
        """
        with self.mock_patch_request() as mock_request:
            mock_request.session_id = time.time()
            mock_request.env = self.env
            mock_request.httprequest.host = self.host_url
            mock_request.httprequest.referrer = self.referrer_url
            res = self.partner1.add_count_view(self.partner2, mock_request)
            self.assertEqual(self.referrer_name, res.host, msg=inspect.stack()[0][3])

    def test_whenReferrerIsNoneInRequest_thenPartnerHostIshost(self):
        """
        Given a res_partner_count_view is created
        When request referrer is none
        Then the res.partner.count.view stores the name of the host
        """
        with self.mock_patch_request() as mock_request:
            mock_request.session_id = time.time()
            mock_request.env = self.env
            mock_request.httprequest.host = self.host_url
            mock_request.httprequest.referrer = None
            res = self.partner1.add_count_view(self.partner2, mock_request)
            self.assertEqual(self.host_name, res.host, msg=inspect.stack()[0][3])
