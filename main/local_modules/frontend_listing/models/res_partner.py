# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import functools
import logging

from openerp import api, models, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def search_domain(self, search):
        """Return the domain that should be used to when a search is processed.

        :param str search: string used for the search.
        :return: list
        """
        _logger.debug('search domain')
        _logger.debug('search: %s', search)
        domain = []

        for sub_search in search.split(' '):
            _logger.debug('sub search: %s', sub_search)
            domain += [
                '|', '|', '|',
                ('name', 'ilike', sub_search),
                ('city', 'ilike', sub_search),
                ('country_id.name', 'ilike', sub_search),
                ('industry_ids.name', 'ilike', sub_search)
            ]
        _logger.debug('domain: %s', domain)
        return domain

    # query used to get major of details.
    # I had to split the query and to get the industries and the states from another
    # query. I cannot use INNER JOIN as both, industried and states, are optional
    # but when I switch to LEFT OUTER JOIN the map become instable and can't display
    # an empty search.
    # good enough.
    main_query = """
    SELECT
      rp.id,
      rp.partner_latitude,
      rp.partner_longitude,
      rp.small_image_url,
      rp.name,
      rp.id,
      rp.city as city_name,
      res_country.name as country_name
    FROM res_partner as rp
    INNER JOIN res_country
      ON rp.country_id=res_country.id
    WHERE
      rp.id IN ({})
    """

    # Query to get the industries.
    industry_query = """
    SELECT
      rp.id,
      ind.name as ind_name
    FROM res_partner as rp
    LEFT OUTER JOIN res_industry_res_partner_rel AS rpr
      ON rpr.res_partner_id = rp.id
    LEFT OUTER JOIN res_industry as ind
      ON ind.id = rpr.res_industry_id
    WHERE
      rp.id IN ({})
    """

    # Query to get the states.
    state_query = """
    SELECT
      rp.id,
      res_country_state.name as state_name
    FROM res_partner as rp
    LEFT OUTER JOIN res_country_state
      ON rp.state_id=res_country_state.id
    WHERE
      rp.id IN ({})
    """

    def get_partners_dict(self, ids):
        """ Use direct sql request to do a select of a set of fields instead of
        using search() that grab only id.
        The query decreased from several secs to less than 10th of a sec.

        :param list ids: list of id of partner to get details from.
        :return: details of the partners.
        :rtype: list
        """
        cr = self.env.cr
        concatenated_ids = ','.join(str(id_) for id_ in ids)

        # Gather the not optional detail of partners.
        cr.execute(self.main_query.format(concatenated_ids))
        global_details = cr.dictfetchall()

        # Gather the industry
        cr.execute(self.industry_query.format(concatenated_ids))
        industries = cr.dictfetchall()

        # Gather the states
        cr.execute(self.state_query.format(concatenated_ids))
        states = cr.dictfetchall()

        add_details = functools.partial(add_partner_details, industries, states)
        details = map(add_details, global_details)
        return details


def add_partner_details(industries, states, partner_dict):
    """

    :param dict industries:
    :param dict states:
    :param dict partner_dict:
    :rtype: dict
    """
    partner_id = partner_dict['id']
    partner_details = partner_dict
    # if the lat/long is not set they will be None but google asks it to be a
    # number.
    partner_details['partner_latitude'] = partner_details['partner_latitude'] or 0.0
    partner_details['partner_longitude'] = partner_details['partner_longitude'] or 0.0
    partner_details.setdefault('industries', []).extend(
        add_industries(partner_id, industries)
    )
    partner_details['state_name'] = add_state_name(partner_id, states)
    return partner_details


def add_state_name(partner_id, states):
    """

    :param int partner_id:
    :param dict states:
    :rtype: str
    """
    state = [
        state_['state_name'] for state_ in states
        if state_['id'] == partner_id
    ]
    if state:
        return state[0]
    return ''


def add_industries(partner_id, industries):
    """

    :param int partner_id:
    :param dict industries:
    :rtype: list
    """
    return [
        str(industry['ind_name']) for industry in industries
        if industry['id'] == partner_id
    ]
