import logging
import os
import simplejson
import ast
from openerp.addons.frontend_base.controllers.base import Base, FrontendBaseError
from openerp.http import request

logger = logging.getLogger(__name__)


class IframeHostError(FrontendBaseError):
    """Base exception for the module."""
    pass


class NotAllowHostFrontendBaseError(IframeHostError):
    """Exception that should be raised if the host name is not allowed to
    display the iframe.
    """

    def __init__(self, host_name):
        super(NotAllowHostFrontendBaseError, self).__init__(
            'The host "{host_name}" is not allowed to display the iframe.'.format(
                host_name=host_name
            )
        )


class NotCompatibleSearchDomainFrontendBaseError(IframeHostError):
    """Exception that should be raised when the search domain from website.iframe.host
    is not compatible and cannot be turned into list/tuple.
    """

    def __init__(self, search_domain):
        super(NotCompatibleSearchDomainFrontendBaseError, self).__init__(
            '"{search_domain}" cannot be turned into a search domain.'.format(
                search_domain=search_domain)
        )


class WebsiteIframe(Base):

    def get_config(self):
        """Lazily get the config file of the module.

        :rtype: dict
        """
        current_folder = os.path.dirname(__file__)
        with open(os.path.join(current_folder, '..', 'static', 'config.json'),
                  'r') as file_:
            return simplejson.load(file_)

    def get_iframe_host(self):
        """Find if the host has a special SearchDomain.

        :rtype: Record
        """
        host_name = request.httprequest.host
        website_iframe_host_pool = request.env['website.iframe.host']
        iframe_host = website_iframe_host_pool.search(
            [('host', '=', host_name)], limit=1
        )
        # TODO: put the whitelisted_hosts in the database.
        valid_host = (not iframe_host == website_iframe_host_pool) and \
                     (host_name not in self.get_config()['whitelisted_hosts'])

        if not valid_host:
            raise NotAllowHostFrontendBaseError(host_name)

        logger.debug('get_iframe_host: %s', iframe_host)
        return iframe_host

    def get_company_domain(self, search, company_status='open'):
        search_domain = super(WebsiteIframe, self).get_company_domain(
            search, company_status=company_status
        )

        iframe_host = self.get_iframe_host()

        if iframe_host:
            search_domain.search.extend(self.get_additional_search_domain(iframe_host))

        return search_domain

    def is_website_navbar_display(self):
        """Set up the display of the navbar according to the settings of the current
        host.

        :rtype: bool
        :return: if the navbar will be displayed or not.
        """
        iframe_host = self.get_iframe_host()
        logger.debug('iframe_host.navbar; %s', iframe_host.navbar)
        return iframe_host.navbar if iframe_host else True

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

        logger.debug('get_company_domain extension: %s', additional_search_domain)
        return additional_search_domain

    def add_display_navbar_setting(self, values):
        values['display_navbar'] = self.is_website_navbar_display()
        logger.debug('display navbar? %s', values['display_navbar'])
        return values

    def get_map_data(self, *args, **kwargs):
        values = super(WebsiteIframe, self).get_map_data(*args, **kwargs)
        return self.add_display_navbar_setting(values)

    def get_list_data(self, *args, **kwargs):
        values = super(WebsiteIframe, self).get_list_data(*args, **kwargs)
        return self.add_display_navbar_setting(values)
