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
import mock
from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites interaction between partner and res.partner.count.*"""

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.partner1 = self.partner_pool.create({'name': 'partner1'})
        self.partner2 = self.partner_pool.create({'name': 'partner2'})

    def test_add_count_view(self):
        """Test the entry res.partner.count.view is created."""
        request = mock.MagicMock(name='mock_request')
        request.httprequest.remote_addr = ip = '127.0.0.666'
        request.httprequest.host = host = 'travis'
        res = self.partner1.add_count_view(self.partner2, request)
        self.assertEqual(self.partner1, res.active_partner_id)
        self.assertEqual(self.partner2, res.passive_partner_id)
        self.assertEqual(host, res.host)
        self.assertEqual(ip, res.ip)
