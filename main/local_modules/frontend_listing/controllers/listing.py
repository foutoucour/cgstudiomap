# -*- coding: utf-8 -*-
import logging
import pprint

import simplejson
from datadog import statsd
from openerp.addons.frontend_base.controllers.base import Base
from openerp.addons.frontend_base.models.caches import caches
from openerp.addons.web import http
from openerp.addons.website.models.website import hashlib

from openerp.http import request, werkzeug

_logger = logging.getLogger(__name__)
cache = caches.get('cache_1h')


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


def image_url(record, field, size=None):
    """Returns a local url that points to the image field of a given browse record."""
    model = record._name
    sudo_record = record.sudo()
    id_ = '%s_%s' % (
        record.id,
        hashlib.sha1(
            sudo_record.write_date or sudo_record.create_date or ''
        ).hexdigest()[0:7]
    )
    size = '' if size is None else '/%s' % size
    return '/website/image/%s/%s/%s%s' % (model, id_, field, size)


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
        _logger.debug('search: %s', search)
        _logger.debug('company_status: %s', company_status)
        partners = self.get_partners(
            request.env['res.partner'],
            search=search,
            company_status=company_status
        )
        _logger.debug('partners: %s', pprint.pformat(partners))

        details = simplejson.dumps(
            [
                {
                    'logo': '<img itemprop="image" '
                            'class="img img-responsive" '
                            'src="{0}"'
                            '/>'.format(image_url(partner, 'image_small')),
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
        _logger.debug('details: %s', details)
        return details

    @statsd.timed('odoo.frontend.list.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(map_url, type='http', auth="public", website=True)
    def map(self, company_status='open', search='', **post):
        """Render the list of studio under a map."""
        url = self.map_url
        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        partners = self.get_partners(
            request.env['res.partner'],
            search=search,
            company_status=company_status
        )

        geoloc = simplejson.dumps(
            {
                partner.id: [
                    partner.partner_latitude,
                    partner.partner_longitude,
                    partner.info_window(company_status),
                ]
                for partner in partners
                }
        )
        _logger.debug(geoloc)
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

    @statsd.timed('odoo.frontend.map.time',
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
