# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging
import random
from copy import deepcopy
from openerp import api, models, fields
from openerp.addons.website.models.website import hashlib

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SearchDomain(object):
    """Represent arguments of a search.

    It has been set to be able to pass all the data needed to do a search or a
    search_count.
    """

    def __init__(self, search, order='', limit=None):
        """

        :param list search: the search for the domain.
        :param str order: the ordering.
        :param int limit: the limit
        """
        self.search = search
        self.order = order
        self.limit = limit


class ResPartnerDomain(models.Model):
    """Definition of search domains for partners."""
    _inherit = 'res.partner'

    #: represent the limit for the domain with latest notion.
    latest_companies_limit = 20

    @property
    def active_companies_domain(self):
        """Return the domain that should be used to filter for active companies.

        :rtype: SearchDomain
        """
        return SearchDomain([('active', '=', True), ('is_company', '=', True)])

    @property
    def closed_companies_domain(self):
        """Return the domain that should be used to filter for companies out of business.

        :rtype: SearchDomain
        """
        domain = deepcopy(self.active_companies_domain)
        domain.search.extend([('state', '=', 'closed')])
        return domain

    @property
    def open_companies_domain(self):
        """Return the domain that should be used to filter for open companies.

        :rtype: SearchDomain
        """
        domain = deepcopy(self.active_companies_domain)
        domain.search.extend([('state', '=', 'open')])
        return domain

    @property
    def latest_created_companies_domain(self):
        """Return the domain that should be used to filter for latest created companies.

        :rtype: SearchDomain
        """
        domain = deepcopy(self.open_companies_domain)
        domain.order = 'create_date desc'
        domain.limit = self.latest_companies_limit
        return domain

    @property
    def latest_updated_companies_domain(self):
        """Return the domain that should be used to filter for latest updated companies.

        :rtype: SearchDomain
        """
        domain = deepcopy(self.open_companies_domain)
        domain.order = 'write_date desc'
        domain.limit = self.latest_companies_limit
        return domain

    @staticmethod
    def search_domain(search):
        """Return the domain that should be used to when a search is processed.

        :param str search: string used for the search.
        :return: list
        """
        logger.debug('Search: %s', search)
        domain = []
        for sub_search in map(lambda s: s.strip(), search.split(',')):
            domain += [
                '|', '|', '|', '|',
                ('name', 'ilike', sub_search),
                # Use perfect match for cities, countries and industries
                # to avoid false results like https://github.com/cgstudiomap/cgstudiomap/issues/700
                ('city', '=ilike', sub_search),
                ('country_id.name', '=ilike', sub_search),
                ('state_id.name', '=ilike', sub_search),
                ('industry_ids.name', '=ilike', sub_search)
            ]
        logger.debug('domain: %s', domain)
        return domain

    def get_company_domain(self, search, company_status='open'):
        """get the domain to use for the given parameters.

        :param str search: search to filter with
        :param str company_status: main status of the companies to filter out.
        :rtype: SearchDomain instance
        """
        search_domains = {
            'active': self.active_companies_domain,
            'open': self.open_companies_domain,
            'closed': self.closed_companies_domain,
            'latest_updated': self.latest_updated_companies_domain,
            'latest_created': self.latest_created_companies_domain,
        }

        search_domain = search_domains.get(company_status, search_domains['open'])
        if search:
            search_domain.search.extend(self.search_domain(search))

        return search_domain


class ResPartner(models.Model):
    _inherit = 'res.partner'

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
                self.active_companies_domain.search +
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
        """Force to reset small_image_url to be reset if image is set to the
        partner.
        """
        logger.debug('vals: %s', vals)

        if 'image' in vals:
            vals.update({'small_image_url': False})
            logger.debug('updated vals: %s', vals)

        return super(ResPartner, self).write(vals)

    partner_url_pattern = '/directory/company/{0}'
    partner_url = fields.Char('Partner url', compute='partner_url_link')

    @api.one
    def partner_url_link(self):
        """Return the link to the page of the current partner."""
        self.partner_url = self.partner_url_pattern.format(self.id)

    def link_to_studio_page(self, partner_url, link_text):
        """build the html tag to use to have a link to the page studio of a partner.

        :param str partner_url: url to the page of a partner.
        :param str|unicode link_text: text displayed as the link.
        :return: <a> tag
        :rtype: str
        """
        return '<a href="{0}">{1}</a>'.format(partner_url, link_text.encode('utf8'))

    def info_window(self, company_status='open'):
        """Build the info window for the google map."""
        title = (
            '<div id="iw-container">'
            '<div class="iw-title"><a href="{0}">{1}</a></div>'
        ).format(self.partner_url, self.name.encode('utf8'))

        body = '<div class="iw-content">'
        body += '<p>{0}</p>'.format(self.location.encode('utf8'))
        body += ' '.join(
            [
                ind.tag_url_link(company_status=company_status)
                for ind in self.industry_ids
            ]
        )
        body += '</div>'
        footer = (
            '<div id="map_info_footer"><a href="{0}">More ...</a></div></div>'
        ).format(self.partner_url)

        return title + body + footer

    def info_window_details(self,
                            id_,
                            name,
                            industries,
                            company_status,
                            city=None,
                            state=None,
                            country=None):
        """Build the info window for the google map."""
        industry_pool = self.env['res.industry']
        partner_url = self.partner_url_pattern.format(id_)
        title = (
            '<div id="iw-container">'
            '<div class="iw-title">{0}</div>'
        ).format(self.link_to_studio_page(partner_url, name))
        body = '<div class="iw-content">'
        location = self.get_location(city, state, country)
        body += '<p>{0}</p>'.format(location.encode('utf8'))
        body += ' '.join(
            [
                industry_pool.tag_url_link_details(ind_name_, company_status)
                for ind_name_ in industries
            ]
        )
        body += '</div>'
        footer = (
            '<div id="map_info_footer">{0}</div></div>'
        ).format(self.link_to_studio_page(partner_url, 'More ...'))
        return title + body + footer

    small_image_url = fields.Char('Url to the small image of the partner.')

    @api.model
    def get_small_image_url(self):
        """Returns a local url that points to the image field of a
        given browse record.

        :return: str, url of the image.
        """
        model = self._name
        sudo_record = self.sudo()
        id_ = '%s_%s' % (
            self.id,
            hashlib.sha1(
                sudo_record.write_date or sudo_record.create_date or ''
            ).hexdigest()[0:7]
        )
        return '/website/image/%s/%s/%s' % (model, id_, 'image_small')

    @api.multi
    def write(self, vals):
        """Make sure the small_url is set when a partner is updated."""
        if 'small_image_url' not in vals:
            vals['small_image_url'] = self.get_small_image_url()

        if vals.get('image', None) is False:
            vals['small_image_url'] = False

        return super(ResPartner, self).write(vals)

    @staticmethod
    def get_location(city=None, state=None, country=None):
        """Return the concatenation of city, state and country."""
        elements = []
        for element in (city, state, country):
            if element:
                elements.append(element)
        return ', '.join(elements)
