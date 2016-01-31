# -*- coding: utf-8 -*-
import logging

import simplejson
from datadog import statsd
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website
from openerp.addons.website.models.website import hashlib

from openerp.http import request, werkzeug

_logger = logging.getLogger(__name__)


class QueryURL(object):
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
                if isinstance(v, list) or isinstance(v, set):
                    l.append(werkzeug.url_encode([(k, i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k, v)]))
        if l:
            path += '?' + '&'.join(l)
        return path


def small_image_url(record, field):
    """Returns a local url that points to the image field of a given browse record."""
    if not record.small_image_url:
        _logger.debug('No small image url for %s', record.id)
        model = record._name
        sudo_record = record.sudo()
        id_ = '%s_%s' % (
            record.id,
            hashlib.sha1(
                sudo_record.write_date or sudo_record.create_date or ''
            ).hexdigest()[0:7]
        )
        record.small_image_url = '/website/image/%s/%s/%s' % (model, id_, field)
        # else:
        # _logger.debug('Great found small image url for %s!', record.id)

    return record.small_image_url

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
