# -*- coding: utf-8 -*-
from openerp.tests import common


class TestResPartner(common.TransactionCase):
    """Test suites interaction between partner and res.partner.count.*"""

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.partner = self.partner_pool.create({'name': 'partner1'})

    def test_whenTheGeolocationFails_thenTheResultStoredIsOutSideOfCoordRange(self):
        """
        Given the geo location is a success
        Given the user is located at 34.0,43.0
        When the function is called
        Then a new res.partner.locate_me_stats is returned
        Then the result has the geo location details
        """
        success = True
        latitude = 34.0
        longitude = 42.0
        res = self.partner.add_locate_me_view(success, latitude, longitude)
        self.assertEqual(self.partner, res.user_id)
        self.assertEqual(success, res.success)
        self.assertEqual(latitude, res.latitude)
        self.assertEqual(longitude, res.longitude)

    def test_whenTheGeolocationIsSuccess_thenTheGeolocationIsStored(self):
        """
        Given the geo location is a failure
        Given the user is located at 34.0,43.0
        When the function is called
        Then a new res.partner.locate_me_stats is returned
        Then the result has some coordinate outside of latitude and longitude range
        """
        success = False
        latitude = 34.0
        longitude = 42.0
        res = self.partner.add_locate_me_view(success, latitude, longitude)
        self.assertEqual(self.partner, res.user_id)
        self.assertFalse(res.success)
        self.assertFalse(res.latitude)
        self.assertFalse(res.longitude)
