# -*- coding: utf-8 -*-
import logging

import simplejson
from datadog import statsd
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TERM_CASE_PATTERN = "{field} ilike '%{term}%'"

PARTNER_CONDITION = "is_company is True AND state = 'open' AND active is True"
#: In the case of countries, we want to list only the countries that have partner related to it.
COUNTRY_CASE = (
    'SELECT DISTINCT res_country.name as value FROM res_partner'
    ' INNER JOIN res_country'
    ' ON res_partner.country_id=res_country.id'
    ' WHERE {0} AND {1}'
)

INDUSTRY_CASE = (
    "SELECT DISTINCT res_industry.name as value FROM res_partner"
    " LEFT OUTER JOIN res_industry_res_partner_rel AS rpr ON rpr.res_partner_id = res_partner.id"
    " LEFT OUTER JOIN res_industry ON res_industry.id = rpr.res_industry_id"
    ' WHERE {0} AND {1}'
)

STATE_CASE = (
    'SELECT DISTINCT res_country_state.name as value FROM res_partner'
    ' INNER JOIN res_country_state'
    ' ON res_partner.state_id=res_country_state.id'
    ' WHERE {0} AND {1}'
)


def build_query(term, field, table, where_condition=None):
    """

    :param str term:
    :param str field:
    :param str table:
    :param str|None where_condition:
    :return:
    """
    query_pattern = "SELECT {field} as value FROM {table}".format(
        field=field, table=table
    )
    term_case = TERM_CASE_PATTERN.format(field=field, term=term)
    # filter out Nones and empty
    conditions = ' AND '.join(filter(lambda x: bool(x), (term_case, where_condition)))
    return ' WHERE '.join(filter(lambda x: bool(x), (query_pattern, conditions)))


def select_from_term(term):
    """

    :param str term:
    :return:
    """
    cr = request.env.cr
    cases = (
        ('name', 'res_partner', PARTNER_CONDITION),
        # ('name', 'res_country_state'), # TODO: states are not considered by the search engine.
        ('city', 'res_partner', 'is_company is True AND city is not null')
    )

    sub_queries = [build_query(term, *case) for case in cases]
    sub_queries.append(
        COUNTRY_CASE.format(PARTNER_CONDITION, TERM_CASE_PATTERN.format(field='res_country.name', term=term))
    )
    sub_queries.append(
        INDUSTRY_CASE.format(PARTNER_CONDITION, TERM_CASE_PATTERN.format(field='res_industry.name', term=term))
    )
    sub_queries.append(
        STATE_CASE.format(PARTNER_CONDITION, TERM_CASE_PATTERN.format(field='res_country_state.name', term=term))
    )

    # Alphabetical order for the results
    query = '{0} ORDER BY value'.format(' UNION '.join(sub_queries))
    logger.debug('query: %s', query)
    cr.execute(query)
    result = [r['value'] for r in cr.dictfetchall()]
    logger.debug('Result from SELECT: %s', result)
    return result


class Ajax(Website):
    """Ajax calls for the search bar."""

    @statsd.timed('odoo.frontend.ajax.get_auto_complete_search_values',
                  tags=['frontend', 'frontend:search_bar', 'ajax'])
    @http.route('/ajax/search_bar/get_auto_complete_search_values',
                type='http', methods=['POST'])
    def get_auto_complete_search_values(self, term=None):
        """Ajax call to get the value for the auto-complete of the search bar.

        :rtype: json
        """
        logger.debug('Term: %s', term)
        json = simplejson.dumps(select_from_term(term) if term else [], ensure_ascii=False).encode('utf8')
        logger.debug('Json that will be sent to browser: %s', json)
        return json
