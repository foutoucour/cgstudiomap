# -*- coding: utf-8 -*-
import logging
import simplejson
from datadog import statsd
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request, werkzeug

_logger = logging.getLogger(__name__)


class QueryURL(object):
    """Class that represents query of a url and allow to keep the arguments
    throught the calls.
    """

    def __init__(self, path='', **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        for k, v in self.args.items():
            kw.setdefault(k, v)
        l = []
        for k, v in kw.items():
            if v:
                if isinstance(v, (list, set)):
                    l.append(werkzeug.url_encode([(k, i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k, v)]))
        if l:
            path += '?' + '&'.join(l)
        return path


class FrontendBaseError(Exception):
    """Base exception for the module."""
    pass


class Base(Website):
    """Representation of the homepage of the website."""

    def get_company_domain(self, search, company_status='open'):
        """get the domain to use for the given parameters.

        :param str search: search to filter with
        :param str company_status: main status of the companies to filter out.
        :rtype: SearchDomain instance
        """
        partner_pool = request.env['res.partner']
        return partner_pool.get_company_domain(search, company_status)

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
        """Return a json with the count of companies for the search criteria.

        :param str search: search to filter with
        :param str company_status: main status of the companies to filter out.
        :return: json dumps
        """
        partner_pool = request.env['res.partner']
        search_domain = self.get_company_domain(search, company_status)
        return simplejson.dumps(
            {
                'counter': (
                    search_domain.limit and search_domain.limit or
                    partner_pool.search_count(search_domain.search)
                )
            }
        )
