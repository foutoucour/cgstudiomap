# -*- coding: utf-8 -*-
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
        request.httprequest.host = host = 'travis'
        res = self.partner1.add_count_view(self.partner2, request)
        self.assertEqual(self.partner1, res.active_partner_id)
        self.assertEqual(self.partner2, res.passive_partner_id)
        self.assertEqual(host, res.host)
