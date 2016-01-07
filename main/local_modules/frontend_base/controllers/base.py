# -*- coding: utf-8 -*-
import logging

import simplejson
from datadog import statsd
from openerp.addons.frontend_base.models.caches import caches
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request

_logger = logging.getLogger(__name__)

cache = caches.get('cache_3h')


class Base(Website):
    """Representation of the homepage of the website."""

    def get_company_domain(self, search, company_status='open'):
        """get the domain to use for the given parameters.

        :param str search: search to filter with
        :param str status: main status of the companies to filter out.
        :return: domain lise dict.
        """
        partner_pool = request.env['res.partner']
        domains = {
            'active': partner_pool.active_companies_domain,
            'open': partner_pool.open_companies_domain,
            'closed': partner_pool.closed_companies_domain,
        }

        domain = domains[company_status]
        if search:
            domain.extend(partner_pool.search_domain(search))
        _logger.debug('Domain: %s', domain)
        return domain

    @statsd.timed('odoo.frontend.ajax.get_user_count_json',
                  tags=['frontend', 'frontend:base', 'ajax'])
    @http.route('/directory/get_user_count_json',
                type='http', auth="public", methods=['POST'], website=True)
    def get_user_count_json(self):
        """Return a json with the count of users for the search criteria
        :return: json dumps
        """
        user_pool = request.env['res.users']
        return simplejson.dumps(
            {'counter': user_pool.get_number_active_users()}
        )

    @statsd.timed('odoo.frontend.ajax.get_company_count_json',
                  tags=['frontend', 'frontend:base', 'ajax'])
    @http.route('/directory/get_company_count_json',
                type='http', auth="public", methods=['POST'], website=True)
    def get_company_count_json(self, search='', company_status='active'):
        """Return a json with the count of companies for the search criteria

        :param str search: search to filter with
        :param str status: main status of the companies to filter out.
        :return: json dumps
        """
        partner_pool = request.env['res.partner']
        return simplejson.dumps(
            {
                'counter': partner_pool.search_count(
                    self.get_company_domain(search, company_status)
                )
            }
        )
