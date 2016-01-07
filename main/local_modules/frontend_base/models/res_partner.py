# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging
import random

from caches import clear_caches
from openerp import api, models, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @property
    def active_companies_domain(self):
        """Return the domain that should be used to filter for active companies.

        :return: list
        """
        return [
            ('active', '=', True),
            ('is_company', '=', True),
        ]

    @property
    def closed_companies_domain(self):
        """Return the domain that should be used to filter for companies out of business.

        :return: list
        """
        return self.active_companies_domain + [('state', '=', 'closed')]

    @property
    def open_companies_domain(self):
        """Return the domain that should be used to filter for open companies.

        :return: list
        """
        return self.active_companies_domain + [('state', '=', 'open')]

    @api.model
    def get_active_companies(self):
        """Return recordsets of all the active companies.

        :return: recordset.
        """
        return self.search(self.active_companies_domain)

    @api.model
    def get_number_active_companies(self):
        """Return the number of active companies.

        :return: int
        """
        return len(self.get_active_companies())

    @api.model
    def get_closed_commpanies(self):
        """Return recordsets of all the companies under the closed status.

        :return: recordset.
        """
        return self.search(self.open_companies_domain)

    @api.model
    def get_open_commpanies(self):
        """Return recordsets of all the companies under the open status.

        :return: recordset.
        """
        return self.search(self.open_companies_domain)

    @api.model
    def get_most_popular_studios(self, sample_):
        """Return a list of partners that have a logo.

        The list is filtered to just returns partner that match:
        - is active
        - is a company
        - is not the partner related to cgstudiomap
        - has an image.
        :return: list of partner records.
        """
        company_pool = self.env['res.company']
        # #294
        # Looking for cgstudiomap to avoid to have it displayed.
        # cgstudiomap is actually the partner linked to the res.company
        # of the instance.
        # looking for the first (and only so far) res.company
        company = company_pool.browse(1)

        # https://github.com/cgstudiomap/cgstudiomap/issues/177
        # search return a recordset and we cannot do len() on it.
        partners = [
            partner for partner in self.search(
                self.active_companies_domain +
                [
                    ('id', '!=', company.partner_id.id),
                    ('image', '!=', False)
                ]
            )
            ]

        # doing kind of unittest in here as I do not know how to
        # do unittest with request :(
        assert company.partner_id.id not in [p.id for p in partners], (
            'cgstudiomap is in the most popular studio list'
        )
        return random.sample(partners, min(len(partners), sample_))

    @api.multi
    def write(self, vals):
        """Force to clear caches when a partner is updated."""
        clear_caches()
        return super(ResPartner, self).write(vals)

    @api.model
    def create(self, vals):
        """Force to clear caches when a new partner is created."""
        clear_caches()
        return super(ResPartner, self).create(vals)

    partner_url = fields.Char('Partner url', compute='partner_url_link')

    @api.one
    def partner_url_link(self):
        """Return the link to the page of the current partner."""
        self.partner_url = (
            '/web#id={0}&view_type=form&model=res.partner'.format(self.id)
        )

    info_window = fields.Char('Info Window', compute='info_window_code')

    @api.one
    def info_window_code(self):
        """Build the info window for the google map."""
        _logger.debug('')
        _logger.debug('self: %s', self)
        _logger.debug('self.name: %s', self.name)
        _logger.debug('self.name (utf8): %s', self.name.encode('utf8'))
        _logger.debug('self.location: %s', self.location)
        _logger.debug('tag url: %s', ' '.join([ind.tag_url for ind in self.industry_ids]))
        _logger.debug('self.partner_url: %s', self.partner_url)
        title = '<div id="map_info_header"><h4>{0}</h4></div>'.format(
            self.name.encode('utf8')
        )
        body = '<div id="map_info_content">'
        body += '<p>{0}</p>'.format(self.location.encode('utf8'))
        body += ' '.join(
            [ind.tag_url.encode('utf8') for ind in self.industry_ids]
        )
        body += '</div>'
        footer = '<div id="map_info_footer"><a href="{0}">More ...</a></div>'.format(
            self.partner_url
        )
        msg = title + body + footer
        self.info_window = msg

    location = fields.Char('Location', compute='location_code')

    @api.one
    def location_code(self):
        """Return the concatenation of city, state and country."""
        self.location = ''.join([
            self.city and '{0}, '.format(self.city.encode('utf8')) or '',
            self.state_id and '{0}, '.format(
                self.state_id.name.encode('utf8')) or '',
            '{0}'.format(self.country_id.name.encode('utf8')),
        ])
