# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp.addons.web import http
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)

from openerp.http import request

_logger = logging.getLogger(__name__)


class Studio(Base):
    """Representation of the homepage of the website."""
    studio_url = '/directory/company'


    @statsd.timed('odoo.frontend.studio.time',
                  tags=['frontend', 'frontend:studio'])
    @http.route('{0}/<model("res.partner"):partner>'.format(studio_url),
                type='http', auth="public", website=True)
    def main(self, partner, mode='view'):
        """Dispatch between the different modes of the page.

        :param str mode: mode the page is viewed. Default: view.
            Can be view, edit, create.

        :return: request.render
        """
        _logger.debug('main')
        _logger.debug('partner: %s', partner)
        _logger.debug('mode: %s', mode)
        # env = request.env
        # partner_pool = env['res.partner']
        url = '{0}/{1}'.format(self.studio_url, partner.id)
        keep = QueryURL(url, mode=mode)
        country = partner.country_id
        values = {
            'partner': partner,
            'partners': partner.get_studios_from_same_location(4),
            'filter_domain': country.name,
            'mode': mode,
            'keep': keep,
        }
        return request.website.render("frontend_studio.view", values)
