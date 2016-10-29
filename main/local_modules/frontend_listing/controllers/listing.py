# -*- coding: utf-8 -*-
import logging
import time

import simplejson
from cachetools import TTLCache, cached
from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (
    Base,
    small_image_url,
    QueryURL,
)
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
    """Representation of the page listing companies.

    Pages of listing are cached using list_cache and map_cache. That is
    because there is a lot of data to load and many because of the build of
    the list object from this data.

    To manage the cache, the attribute `force_reset_cache` has been set.
    It allows a user to force to rebuild the cache if for example a massive
    update on data has been operated.

    To use the force_cache_reset the url should look like:
    * to reset the cache of the map
        /directory?force_cache_reset=1
    * to reset the cache of the list
        /directory/list?force_cache_reset=1
    """
    # the cache are set to None so they are set at the first call of the pages.
    list_cache = None
    map_cache = None
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
        :return: json dumps
        """

        @cached(self.list_cache)
        def build_details(partners):
            """Gather the details to build later the table of companies.

            :param list partners: recordsets of partner to gather the details
                from.
            :return: json dump.
            """
            return simplejson.dumps(
                [
                    {
                        'logo': '<img itemprop="image" '
                                'class="img img-responsive" '
                                'src="{0}"'
                                '/>'.format(
                            small_image_url(partner, 'image_small')),
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
                        'city': partner.city,
                        'state_name': partner.state_id.name,
                        'country_name': partner.country_id.name,
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
        _logger.debug(
            'cache.currsize: %s', self.list_cache.currsize
        )
        statsd.gauge(
            'odoo.frontend.list_cache_currsize',
            self.list_cache.currsize
        )
        _logger.debug('dump timing: %s', time.time() - t1)
        return details

    def get_map_data(self,
                     company_status='open',
                     search='',
                     force_cache_reset=False,
                     **post):
        """Get the data to render the map.
        :param bool force_cache_reset: if the cache of the
                                       page needs to be reset.
        :rtype: dict
        """
        def build_details(partners):
            """Gather details from partners to be displayed on the map.

            :param recordset partners: partners to gather the details from.
            :return: json dump.
            """
            sql_request = """
            SELECT
              rp.id,
              rp.partner_latitude,
              rp.partner_longitude,
              rp.name,
              rp.id,
              rp.city as city_name,
              res_country_state.name as state_name,
              res_country.name as country_name,
              ind.name as ind_name
            FROM res_partner as rp
            INNER JOIN res_country_state
              ON rp.state_id=res_country_state.id
            INNER JOIN res_country
              ON rp.country_id=res_country.id
            INNER JOIN res_industry_res_partner_rel AS rpr
              ON rpr.res_partner_id = rp.id
            INNER JOIN res_industry as ind
              ON ind.id = rpr.res_industry_id
            WHERE
              rp.id IN ({})
            """.format(','.join(str(p.id) for p in partners))
            cr = partners.env.cr
            cr.execute(sql_request)
            details = {}

            # Unify the list of partner and gather the industries
            for partner in cr.dictfetchall():

                if partner['id'] not in details:
                    details[partner['id']] = partner

                details[partner['id']].setdefault('industries', []).append(
                    partner['ind_name'])

            return simplejson.dumps(
                {
                    partner['id']: [
                        partner['partner_latitude'],
                        partner['partner_longitude'],
                        partners.info_window_details(
                            partner['id'],
                            partner['name'],
                            partner['industries'],
                            company_status,
                            city=partner['city_name'],
                            state=partner['state_name'],
                            country=partner['country_name']
                        ),
                    ]
                    for partner in details.itervalues()
                    }
            )

        url = self.map_url
        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        partner_pool = request.env['res.partner']
        partners = self.get_partners(
            partner_pool,
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
                      force_cache_reset=False,
                      **post):
        """
        :param bool force_cache_reset: if the cache of the
                                       page needs to be reset.
        """
        _logger.debug('force_cache_reset: %s', force_cache_reset)

        if self.list_cache is None or force_cache_reset:
            _logger.debug('Reset the cache list_cache')
            self.list_cache = reset_cache()

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
