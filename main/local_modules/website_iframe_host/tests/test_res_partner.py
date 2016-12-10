# -*- coding: utf-8 -*-
import functools

import mock
import unittest

from openerp.tests import common
from openerp.addons.website_iframe_host.models.res_partner import (
    add_target_blank_to_a,
)

mock_patch_light_hosting = functools.partial(
    mock.patch,
    'openerp.addons.website_iframe_host.models.res_partner.is_website_light_hosting'
)

pattern_a_target_blank = '<a target="_blank" '


class TestAddTargetBlankToA(unittest.TestCase):
    """Test suites for the function add_target_blank_to_a."""

    def setUp(self):
        self.func = add_target_blank_to_a

    def test_whenThereAInTheHTMLCode_changeItWithBlanks(self):
        """Test the blanks are added."""
        html_code_with_a = (
            '<div id="iw-container"><div class="iw-title">'
            '<a href="/directory/company/1">toto</a></div>'
            '<div class="iw-content"><p>Montréal, Québec, Canada</p>'
            '<a itemprop="name" href="/directory?company_status=open&search=Animation">'
            '<span class="label label-info">Animation</span></a></div>'
            '<div id="map_info_footer"><a href="/directory/company/1">'
            'More ...</a></div></div>'
        )

        html_code_with_a_blank = (
            '<div id="iw-container"><div class="iw-title">'
            '<a target="_blank" href="/directory/company/1">toto</a></div>'
            '<div class="iw-content"><p>Montréal, Québec, Canada</p>'
            '<a target="_blank" itemprop="name" '
            'href="/directory?company_status=open&search=Animation">'
            '<span class="label label-info">Animation</span></a></div>'
            '<div id="map_info_footer">'
            '<a target="_blank" href="/directory/company/1">More ...</a></div></div>'
        )
        self.assertEqual(html_code_with_a_blank, self.func(html_code_with_a))


class TestResPartnerLink(common.TransactionCase):
    """Test suite for the method link_to_studio_page"""

    def setUp(self):
        super(TestResPartnerLink, self).setUp()
        self.func = self.env['res.partner'].link_to_studio_page
        self.partner_url = 'http://www.example.com/page/33'
        self.link_text = 'link'

    @mock_patch_light_hosting()
    def test_whenIFrameIsLightHosting_linkHasBlankTarget(self, mock_light_hosting):
        """Test the info windows are updated for light_hosting iframes"""
        mock_light_hosting.return_value = True
        ret = self.func(self.partner_url, self.link_text)
        self.assertIn(pattern_a_target_blank, ret)

    @mock_patch_light_hosting()
    def test_whenIFrameIsNotLightHosting_noChange(self, mock_light_hosting):
        """Test the info windows is not changed if the iframe is not light hosting."""
        mock_light_hosting.return_value = False
        ret = self.func(self.partner_url, self.link_text)
        self.assertNotIn(pattern_a_target_blank, ret)


class TestResPartnerInfoWindowDetails(common.TransactionCase):
    """Test suite for the method info_window_details overcharge."""

    def setUp(self):
        super(TestResPartnerInfoWindowDetails, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.func = self.partner_pool.info_window_details

    @mock_patch_light_hosting()
    def test_whenIFrameIsLightHosting_infoWindowsHasBlanks(self, mock_light_hosting):
        """Test the info windows are updated for light_hosting iframes"""
        mock_light_hosting.return_value = True
        ret = self.func(
            1, 'toto', ['Animation'], 'open', u'Montréal', u'Québec', 'Canada'
        )
        self.assertIn(pattern_a_target_blank, ret)

    @mock_patch_light_hosting()
    def test_whenIFrameIsNotLightHosting_noChange(self, mock_light_hosting):
        """Test the info windows is not changed if the iframe is not light hosting."""
        mock_light_hosting.return_value = False
        ret = self.func(
            1, 'toto', ['Animation'], 'open', u'Montréal', u'Québec', 'Canada'
        )
        self.assertNotIn(pattern_a_target_blank, ret)
