# -*- coding: utf-8 -*-
import logging

import simplejson
from datadog import statsd
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
    term_case = "{field} ilike '%{term}%'".format(field=field, term=term)
    conditions = ' AND '.join(filter(lambda x: bool(x), (term_case, where_condition)))
    return ' WHERE '.join(filter(lambda x: bool(x), (query_pattern, conditions)))


def select_from_term(term):
    """

    :param str term:
    :return:
    """
    cr = request.env.cr
    cases = (
        ('name', 'res_partner', "is_company is True AND state = 'open'"),
        ('name', 'res_country'),  # TODO: only countries with partners
        ('name', 'res_industry'),  # TODO: only industries with partners
        # ('name', 'res_country_state'), # TODO: only states with partners
        ('city', 'res_partner', 'is_company is True AND city is not null')
    )
    # Alphabetical order for the results
    query = '{0} ORDER BY value'.format(' UNION '.join(build_query(term, *case) for case in cases))
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
                type='http', methods=['GET'])
    def get_auto_complete_search_values(self, term=None):
        """Ajax call to get the value for the auto-complete of the search bar.

        :rtype: json
        """
        logger.debug('Term: %s', term)
        json = simplejson.dumps(select_from_term(term) if term else [], ensure_ascii=False).encode('utf8')
        logger.debug('Json that will be sent to browser: %s', json)
        return json
