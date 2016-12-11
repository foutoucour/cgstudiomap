import functools
import mock
import unittest

import time
from openerp.addons.website_iframe_host.controllers.base import get_host_from_session


def get_module_path(module_name):
    return 'openerp.addons.website_iframe_host.controllers.base.{0}'.format(
        module_name
    )


class TestGetHostFromSessions(unittest.TestCase):
    """Test suite for the get_host_from_session function."""
    module_request_path = get_module_path('request')
    mock_patch_request = functools.partial(mock.patch, module_request_path)

    def setUp(self):
        self.func = get_host_from_session
        self.host = 'cgstudiomap.org'
        self.referrers = (
            # regular
            'http://www.cgstudiomap.org',
            # secured
            'https://www.cgstudiomap.org',
            # no subdomain
            'http://cgstudiomap.org',
            # strange subdomain
            'http://motion.cafe.cgstudiomap.org',
            # long url
            'http://www.cgstudiomap.org/directory/page/3',
            # regular with trailing /
            'http://www.cgstudiomap.org/',
        )
        self.hosts = (
            # regular
            'www.cgstudiomap.org',
            # no subdomain
            'cgstudiomap.org',
            # strange subdomain
            'motion.cafe.cgstudiomap.org',
        )

    @mock_patch_request()
    def test_whenTheFunctionIsCalledForTheFirstTime_referrerIsReturned(self,
                                                                       mock_request):
        """Test the behaviour with single run against the function."""
        for referrer in self.referrers:
            mock_request.httprequest.referrer = referrer
            ret = self.func(time.time())
            self.assertEqual(
                self.host, ret,
                msg=(
                    'The hostname was not extracted as expected from referrer {}: '
                    'expected: {}, returned {}'.format(
                        referrer, self.host, ret
                    )
                )
            )

    @mock_patch_request()
    def test_whenReferrerDoesNotExists_httprequestHostIsReturned(self, mock_request):
        """Test that host is a back up plan for getting the hostname."""
        mock_request.httprequest.referrer = ''
        for hostname in self.hosts:
            mock_request.httprequest.host = hostname
            ret = self.func(time.time())
            self.assertEqual(
                self.host, ret,
                msg=(
                    'The hostname was not extracted as expected from host {}: '
                    'expected: {}, returned {}'.format(
                        hostname, self.host, ret
                    )
                )
            )

    @mock_patch_request()
    def test_whenCalledSeveralTimesWithDifferentSessionID_requestValuesAreUsed(self, mock_request):  # noqa
        """Test that the cache does not work if the session id change"""
        referrer = self.referrers[0]
        mock_request.httprequest.referrer = referrer
        ret = self.func(time.time())
        self.assertEqual(
            self.host, ret, msg='Return should be {}, not {}'.format(self.host, ret)
        )
        referrer = 'http://example.com'
        expected = 'example.com'
        mock_request.httprequest.referrer = referrer
        ret = self.func(time.time())
        self.assertEqual(
            expected, ret, msg='Return should be {}, not {}'.format(expected, ret)
        )

    @mock_patch_request()
    def test_whenCalledSeveralTimesWithSameSessionID_cachedValueUsed(self, mock_request):
        """Test that the cache value is used if same session request host several times.
        """
        referrer = self.referrers[0]
        session_id = time.time()
        mock_request.httprequest.referrer = referrer
        ret = self.func(session_id)
        self.assertEqual(
            self.host, ret, msg='Return should be {}, not {}'.format(self.host, ret)
        )
        referrer = 'http://example.com'
        mock_request.httprequest.referrer = referrer
        ret = self.func(session_id)
        self.assertEqual(
            self.host, ret, msg='Return should be {}, not {}'.format(self.host, ret)
        )

    @mock_patch_request()
    def test_whenGoogleIsReferrer_cgstudiomapIsReturned(self, mock_request):
        """We want to allow google to be the referrer for some call.

        For some reason, we have 500 pages because of google is referrer.
        We do not really have figured out when the case appears but for now we
        set up a fallback for the case so the 500 disappear.

        See: https://github.com/cgstudiomap/cgstudiomap/issues/766
        """
        google_referrers = (
            'http://www.google.ca', 'https://www.google.de'
        )
        mock_request.httprequest.host = self.host
        for referrer in google_referrers:
            mock_request.httprequest.referrer = referrer
            ret = self.func(time.time())
            self.assertEqual(
                self.host, ret, msg='Return should be {}, not {}'.format(self.host, ret)
        )
