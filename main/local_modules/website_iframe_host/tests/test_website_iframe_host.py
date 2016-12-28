import functools
import mock

from openerp.tests import common
import time
from openerp.addons.website_iframe_host.controllers.base import get_host_from_session


def get_module_path(module_name):
    return 'openerp.addons.website_iframe_host.controllers.base.{0}'.format(
        module_name
    )


class TestGetHostFromSessions(common.TransactionCase):
    """Test suite for the get_host_from_session function."""

    def setUp(self):
        super(TestGetHostFromSessions, self).setUp()
        self.func = get_host_from_session
        self.website_iframe_host_pool = self.env['website.iframe.host']

        self.module_request_path = get_module_path('request')
        self.mock_patch_request = functools.partial(mock.patch, self.module_request_path)

        self.hostname = 'cgstudiomap.org'
        self.host = self.website_iframe_host_pool.create(
            {'host': self.hostname, 'search_domain': []}
        )
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

    def test_whenTheFunctionIsCalledForTheFirstTime_referrerIsReturned(self):
        """Test the behaviour with single run against the function."""
        with self.mock_patch_request() as mock_request:
            mock_request.env = self.env
            for referrer in self.referrers:
                mock_request.httprequest.referrer = referrer
                ret = self.func(time.time())
                self.assertEqual(
                    self.host.host, ret.host,
                    msg=(
                        'The hostname was not extracted as expected from referrer {}: '
                        'expected: {}, returned {}'.format(
                            referrer, self.host.host, ret.host
                        )
                    )
                )

    def test_whenReferrerDoesNotExists_httprequestHostIsReturned(self):
        """Test that host is a back up plan for getting the hostname."""
        with self.mock_patch_request() as mock_request:
            mock_request.env = self.env
            mock_request.httprequest.referrer = ''
            for hostname in self.hosts:
                mock_request.httprequest.host = hostname
                ret = self.func(time.time())
                self.assertEqual(
                    self.host.host, ret.host,
                    msg=(
                        'The hostname was not extracted as expected from host {}: '
                        'expected: {}, returned {}'.format(
                            hostname, self.host.host, ret.host
                        )
                    )
                )

    def test_whenCalledSeveralTimesWithDifferentSessionID_requestValuesAreUsed(self):
        """Test that the cache does not work if the session id change.
        """
        with self.mock_patch_request() as mock_request:
            mock_request.env = self.env
            referrer = self.referrers[0]
            mock_request.httprequest.referrer = referrer
            ret = self.func(time.time())
            self.assertEqual(
                self.host.host, ret.host,
                msg='Return should be {}, not {}'.format(self.host.host, ret.host)
            )
            referrer = 'http://example.com'
            expected = 'example.com'

            host_example = self.website_iframe_host_pool.create(
                {'host': expected, 'search_domain': []}
            )
            mock_request.httprequest.referrer = referrer
            ret = self.func(time.time())
            self.assertEqual(
                host_example.host, ret.host,
                msg='Return should be {}, not {}'.format(expected, ret)
            )

    def test_whenCalledSeveralTimesWithSameSessionID_cachedValueUsed(self):
        """Test that the cache value is used if same session request host several times.
        """
        with self.mock_patch_request() as mock_request:
            mock_request.env = self.env
            referrer = self.referrers[0]
            session_id = time.time()
            mock_request.httprequest.referrer = referrer
            ret = self.func(session_id)
            self.assertEqual(
                self.host.host, ret.host,
                msg='Return should be {}, not {}'.format(self.host.host, ret.host)
            )
            referrer = 'http://example.com'
            mock_request.httprequest.referrer = referrer
            ret = self.func(session_id)
            self.assertEqual(
                self.host.host, ret.host,
                msg='Return should be {}, not {}'.format(self.host.host, ret.host)
            )

    def test_whenUnknownReferrer_fallbackToCgstudiomap(self):
        """We want to allow google or facebook to be the referrer for some call.

        For some reason, we have 500 pages because of google is referrer.
        We do not really have figured out when the case appears but for now we
        set up a fallback for the case so the 500 disappear.
        Actually the issue can also happen when the referrer is another than google.
        It seems the issue comes when some referrer to us directly.

        See: https://github.com/cgstudiomap/cgstudiomap/issues/766
        """
        with self.mock_patch_request() as mock_request:
            mock_request.env = self.env
            google_referrers = (
                'http://www.google.ca',
                'https://www.google.de',
                'http://www.facebook.com'
            )
            mock_request.httprequest.host = self.hostname
            for referrer in google_referrers:
                mock_request.httprequest.referrer = referrer
                ret = self.func(time.time())
                self.assertEqual(
                    self.host.host, ret.host,
                    msg='Return should be {}, not {}'.format(self.host.host, ret.host)
                )

    def test_whenReferrerIsNotCgstudiomapButExists_returnIframeHostOfTheOtherHost(self):
        """Test that we can have different iframe.host than cgstudiomap."""
        with self.mock_patch_request() as mock_request:
            mock_request.env = self.env
            referrer = 'http://example.com'
            expected = 'example.com'

            host_example = self.website_iframe_host_pool.create(
                {'host': expected, 'search_domain': []}
            )
            mock_request.httprequest.referrer = referrer
            ret = self.func(time.time())
            self.assertEqual(
                host_example.host, ret.host,
                msg='Return should be {}, not {}'.format(expected, ret)
            )
            self.assertNotEqual(self.host.host, ret.host)
