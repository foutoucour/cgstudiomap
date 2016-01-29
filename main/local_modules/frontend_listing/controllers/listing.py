# -*- coding: utf-8 -*-
import logging

import simplejson
import time
from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (
    Base,
    small_image_url,
    QueryURL,
)
from openerp.addons.web import http
from cachetools import LRUCache, cached

from openerp.http import request

_logger = logging.getLogger(__name__)
list_cache = LRUCache(maxsize=10)
map_cache = LRUCache(maxsize=10)


class Listing(Base):
    """Representation of the page listing companies."""

    map_url = '/directory'
    list_url = '/directory/list'

    def get_partners(self, partner_pool, search='', company_status='open'):
        """Wrapper to be able to cache the result of a search in the
        partner_pool
        """
        return partner_pool.search(
            self.get_company_domain(search, company_status)
        )

    @statsd.timed('odoo.frontend.ajax.get_partner',
                  tags=['frontend', 'frontend:listing', 'ajax'])
    @http.route('/directory/get_partners',
                type='http', auth="public", methods=['POST'], website=True)
    def get_partner_json(self, search='', company_status='open'):
        """Return a json with the partner matching the search

        :param str search: search to filter with
        :return: json dumps
        """
        @cached(list_cache)
        def build_details(partners):
            """Gather the details to build later the table of companies.

            :param recordset partners: partners to gather the details from.
            :return: json dump.
            """
            return simplejson.dumps(
                [
                    {
                        'logo': '<img itemprop="image" '
                                'class="img img-responsive" '
                                'src="{0}"'
                                '/>'.format(small_image_url(partner, 'image_small')),
                        'name': '<a href="{0.partner_url}">{1}</a>'.format(
                            partner, partner.name.encode('utf-8')
                        ),
                        'email': partner.email or '',
                        'industries': ' '.join(
                            [
                                ind.tag_url_link(
                                    company_status=company_status,
                                    listing=True
                                )
                                for ind in partner.industry_ids
                                ]
                        ),
                        'location': partner.location,
                    }
                    for partner in partners
                    ],
            )

        _logger.debug('search: %s', search)
        _logger.debug('company_status: %s', company_status)
        t1 = time.time()
        partners = self.get_partners(
            request.env['res.partner'],
            search=search,
            company_status=company_status
        )
        _logger.debug('Query time: %s', time.time() - t1)
        t1 = time.time()
        details = build_details(partners)
        _logger.debug('cache.currsize: %s', list_cache.currsize)
        _logger.debug('dump timing: %s', time.time() - t1)
        return details

    @statsd.timed('odoo.frontend.map.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(map_url, type='http', auth="public", website=True)
    def map(self, company_status='open', search='', **post):
        """Render the list of studio under a map."""

        @cached(map_cache)
        def build_details(partners):
            """Gather details from partners to be displayed on the map.

            :param recordset partners: partners to gather the details from.
            :return: json dump.
            """
            return simplejson.dumps(
                {
                    partner.name: [
                        partner.partner_latitude,
                        partner.partner_longitude,
                        partner.info_window(company_status),
                    ]
                    for partner in partners
                    }
            )
        url = self.map_url
        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        partners = self.get_partners(
            request.env['res.partner'],
            search=search,
            company_status=company_status
        )

        t1 = time.time()
        geoloc = build_details(partners)
        _logger.debug('dump timing: %s', time.time() - t1)

        values = {
            'geoloc': geoloc,
            'search': search,
            'company_status': company_status,
            'partners': partners,
            'keep': keep,
            'map_url': self.map_url,
            'list_url': self.list_url,
            'url': self.map_url,
        }

        return request.website.render("frontend_listing.map", values)

    @statsd.timed('odoo.frontend.list.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(list_url, type='http', auth="public", website=True)
    def list(self, company_status='open', page=0, search='', **post):
        """Render the list of studio under a table."""
        url = self.list_url

        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        values = {
            'search': search,
            'company_status': company_status,
            'keep': keep,
            'map_url': self.map_url,
            'list_url': self.list_url,
            'url': self.list_url,
        }

        return request.website.render("frontend_listing.list", values)
