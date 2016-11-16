# -*- coding: utf-8 -*-
import logging
import time

import simplejson
from cachetools import TTLCache, cached
from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)
from openerp.addons.web import http

from openerp.http import request

_logger = logging.getLogger(__name__)


def reset_cache(max_size=10, ttl=10800):
    """Reset the given cache.

    :param int max_size: the max number of caches. Default: 10
    :param int ttl: The time max the cache lives. The cache
        will reset itself after this time. Default: 10800 (3hrs)

    :return: cachetools.TTLCache instance.
    """
    return TTLCache(max_size, ttl)


class Listing(Base):
    """Representation of the page listing companies."""
    map_url = '/directory'
    list_url = '/directory/list'

    def get_partners(self, partner_pool, search='', company_status='open'):
        """Wrapper to be able to cache the result of a search in the
        partner_pool.

        :return: record set answering the search criteria.
        """
        search_domain = self.get_company_domain(search, company_status)
        return partner_pool.search(
            search_domain.search,
            order=search_domain.order,
            limit=search_domain.limit
        )

    @statsd.timed('odoo.frontend.ajax.get_partner',
                  tags=['frontend', 'frontend:listing', 'ajax'])
    @http.route('/directory/get_partners',
                type='http', auth="public", methods=['POST'], website=True)
    def get_partner_json(self, search='', company_status='open'):
        """Return a json with the partner matching the search

        :param str search: search to filter with
        :param str company_status: status the search will be done with. Default: open.
        :return: json dumps
        :rtype: dict
        """
        _logger.debug('search: %s', search)
        _logger.debug('company_status: %s', company_status)
        partner_pool = request.env['res.partner']
        partners = self.get_partners(
            partner_pool, search=search, company_status=company_status
        )
        t1 = time.time()
        ids = [p.id for p in partners]
        details = []
        if ids:
            industry_pool = request.env['res.industry']
            details = [
                {
                    'logo': '<img itemprop="image" '
                            'class="img img-responsive" '
                            'src="{0}"'
                            '/>'.format(partner_dict.get('small_image_url', '')),
                    'name': partner_pool.link_to_studio_page(
                        partner_pool.partner_url_pattern.format(partner_dict['id']),
                        partner_dict['name']
                    ),
                    'email': partner_dict.get('email', ''),
                    'industries': ' '.join(
                        industry_pool.tag_url_link_details(
                            ind_name_, company_status, listing=True
                        )
                        for ind_name_ in partner_dict['industries']
                    ),
                    'city': partner_dict.get('city_name', ''),
                    'state_name': partner_dict.get('state_name', ''),
                    'country_name': partner_dict.get('country_name', ''),
                }
                for partner_dict in partner_pool.get_partners_dict(ids)
                ]

        _logger.debug('dump timing: %s', time.time() - t1)
        return simplejson.dumps(details)

    def get_map_data(self,
                     company_status='open',
                     search='',
                     **post):
        """Get the data to render the map.

        :rtype: dict
        """

        url = self.map_url
        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        partner_pool = request.env['res.partner']
        partners = self.get_partners(
            partner_pool, search=search, company_status=company_status
        )

        t1 = time.time()
        ids = [partner.id for partner in partners]
        geoloc = {}
        if ids:
            geoloc = {
                    partner_dict['id']: [
                        partner_dict['partner_latitude'],
                        partner_dict['partner_longitude'],
                        partners.info_window_details(
                            partner_dict['id'],
                            partner_dict['name'],
                            partner_dict['industries'],
                            company_status,
                            city=partner_dict['city_name'],
                            state=partner_dict['state_name'],
                            country=partner_dict['country_name']
                        ),
                    ]
                    for partner_dict in partner_pool.get_partners_dict(ids)
                    }
        _logger.debug('dump timing: %s', time.time() - t1)

        values = {
            'geoloc': simplejson.dumps(geoloc),
            'search': search,
            'company_status': company_status,
            'partners': partners,
            'keep': keep,
            'map_url': self.map_url,
            'list_url': self.list_url,
            'url': self.map_url,
        }
        return values

    @statsd.timed('odoo.frontend.map.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(map_url, type='http', auth="public", website=True)
    def map(self, *args, **kwargs):
        """Render the list of studio under a map."""
        values = self.get_map_data(*args, **kwargs)
        return request.website.render("frontend_listing.map", values)

    def get_list_data(self,
                      company_status='open',
                      page=0,
                      search='',
                      **post):
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
        return values

    @statsd.timed('odoo.frontend.list.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(list_url, type='http', auth="public", website=True)
    def list(self, *args, **kwargs):
        """Render the list of studio under a table."""
        values = self.get_list_data(*args, **kwargs)
        return request.website.render("frontend_listing.list", values)
