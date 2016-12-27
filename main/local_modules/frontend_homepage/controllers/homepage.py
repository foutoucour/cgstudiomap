# -*- coding: utf-8 -*-
import logging
from copy import deepcopy
from collections import defaultdict

from datadog import statsd
from cachetools import TTLCache, cached
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website
from openerp.http import request

_logger = logging.getLogger(__name__)
# cache of 3hrs max.
cache = TTLCache(10, 10800)


class Homepage(Website):
    """Representation of the homepage of the website."""

    @statsd.timed('odoo.frontend.index.time',
                  tags=['frontend', 'frontend:homepage'])
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        """Dispatch between homepage depending on the status of the user."""
        _logger.debug('index')
        uid = request.uid
        public_user_id = request.website.user_id.id
        is_public_user = uid == public_user_id
        _logger.debug('uid: %s', uid)
        _logger.debug('user is public user? %s', is_public_user)
        if is_public_user:
            return self.index_public_user(**kw)
        else:
            return self.index_public_user(**kw)

    def index_public_user(self, **kw):
        """Build the homepage for a public user.
        This homepage is aimed to attract the user to login.
        """

        @cached(cache)
        def get_partners_by_country(countries):
            """Method to be memorized that return the number of partner in a country.

            :param instance countries: record of a country
            :return: country instance: count of partners in the country
            :rtype: dict
            """
            by_countries_ = defaultdict(int)

            search_domain = deepcopy(partner_pool.open_companies_domain)
            for country_ in countries:
                number_partners = partner_pool.search_count(
                    search_domain.search + [('country_id', '=', country_.id)]
                )
                if number_partners:
                    by_countries_[country_] = number_partners

            return by_countries_

        _logger.debug('index_public_user')
        page = 'homepage'
        env = request.env
        partner_pool = env['res.partner']
        # optimisation as it is used in get_partners_by_country
        by_countries = get_partners_by_country(
            request.env['res.country'].search([]))

        values = {
            'page': page,
            'search': '',
            'company_status': 'open',
            'geochart_data': [['Country', 'Popularity']] + [
                [str(country.name), int(value)]
                for country, value in by_countries.items()
            ],
            'partners': partner_pool.get_most_popular_studios(8),
        }
        return request.render('frontend_homepage.homepage', values)

