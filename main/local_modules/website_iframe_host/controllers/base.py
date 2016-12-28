import logging
import ast

import simplejson
from cachetools import cached, LRUCache

from openerp.addons.frontend_base.controllers.base import Base, FrontendBaseError
from openerp.http import request


logger = logging.getLogger(__name__)
cache = LRUCache(maxsize=100)


class IframeHostError(FrontendBaseError):
    """Base exception for the module."""
    def __init__(self, message):
        logger.error(message)
        super(IframeHostError, self).__init__(message)


class NotCompatibleSearchDomainFrontendBaseError(IframeHostError):
    """Exception that should be raised when the search domain from website.iframe.host
    is not compatible and cannot be turned into list/tuple.
    """

    def __init__(self, search_domain):
        super(NotCompatibleSearchDomainFrontendBaseError, self).__init__(
            '"{search_domain}" cannot be turned into a search domain.'.format(
                search_domain=search_domain)
        )


@cached(cache)
def get_host_from_session(session_id):
    """Get the website.iframe.host related to the hostname/referrer
    for the session and cache it to keep the same session under the same host,
     even if the view is done through an iframe.

    Referrers look like _http(s)://(subdomain).(domain)/(route)_
    Hosts look like _(subdomain).(domain)_

    See: https://github.com/cgstudiomap/cgstudiomap/issues/759
    See: https://github.com/cgstudiomap/cgstudiomap/issues/766

    :param int session_id: id of a session.
                           see: https://en.wikipedia.org/wiki/Session_(computer_science)  # noqa
    :return: name of the hostname
    :rtype: str
    """
    # excluded the subdomain from the hostname to ease the maintains.
    # see https://github.com/cgstudiomap/cgstudiomap/issues/730
    exclude_subdomain = lambda host: '.'.join(host.split('.')[-2:])
    website_iframe_host_pool = request.env['website.iframe.host']
    get_website_iframe_host = lambda host_name: website_iframe_host_pool.search(
        [('host', '=', host_name)], limit=1
    )
    logger.debug('session_id: %s', session_id)
    referrer = request.httprequest.referrer
    request_host = request.httprequest.host
    try:
        host = exclude_subdomain(referrer.split('/')[2])
        iframe_host = get_website_iframe_host(host)

        if iframe_host == website_iframe_host_pool:
            raise AttributeError(
                'The referrer "{host}" is not a special case of iframe. '
                'Fallback to host.'.format(host=referrer)
            )

    except (IndexError, AttributeError) as err:
        logger.warning(
            'Referrer does not seems to reliable. Fallback to host. Error: %s', err
        )
        host = exclude_subdomain(request_host)
        iframe_host = get_website_iframe_host(host)

    logger.info('iframe_host: %s', iframe_host)
    logger.info(
        simplejson.dumps(
            {
                'referrer': referrer,
                'request_host': request_host,
                'host': host,
                'iframe_host': str(iframe_host),
                'iframe_host.host': iframe_host.host
            }
        )
    )
    return iframe_host


def get_iframe_host():
    """Find if the host has a special SearchDomain.

    :rtype: Record
    """
    # call to allow the cache to be tested against the session id.
    return get_host_from_session(request.session_id)


def is_website_light_hosting():
    """Check if the host is expecting to have the redirections.

    :rtype: bool
    :return: if the redirection to cgstudiomap should be activated (True).
    """
    iframe_host = get_iframe_host()
    return iframe_host.light_hosting if iframe_host else False


def is_website_navbar_hidden():
    """Set up the hide of the navbar according to the settings of the current
    host.

    :rtype: bool
    :return: if the navbar will be hidden (True) or not.
    """
    iframe_host = get_iframe_host()
    return iframe_host.hide_navbar if iframe_host else False


class WebsiteIframe(Base):

    def get_company_domain(self, search, company_status='open'):
        search_domain = super(WebsiteIframe, self).get_company_domain(
            search, company_status=company_status
        )

        iframe_host = get_iframe_host()

        if iframe_host:
            search_domain.search.extend(self.get_additional_search_domain(iframe_host))

        return search_domain

    def get_additional_search_domain(self, host):
        """Extend the current search_domain according to the settings of the current
        host.

        :param record host: website.iframe.host record
        :rtype: bool
        :return: if the navbar will be displayed or not.
        """
        additional_search_domain = ast.literal_eval(host.search_domain)

        if not isinstance(additional_search_domain, (tuple, list)):
            raise NotCompatibleSearchDomainFrontendBaseError(
                additional_search_domain
            )

        return additional_search_domain

    def add_host_settings(self, values):
        """Add to values the special settings for the iframe hosts.

        :param dict values: rendering values
        :return: values with additional keys/values
        :rtype: dict
        """
        values['hide_navbar'] = is_website_navbar_hidden()
        values['light_hosting'] = is_website_light_hosting()
        return values

    def get_map_data(self, *args, **kwargs):
        """Add the host settings to the map."""
        values = super(WebsiteIframe, self).get_map_data(*args, **kwargs)
        return self.add_host_settings(values)

    def get_list_data(self, *args, **kwargs):
        """Add the host settings to the listing."""
        values = super(WebsiteIframe, self).get_list_data(*args, **kwargs)
        return self.add_host_settings(values)
