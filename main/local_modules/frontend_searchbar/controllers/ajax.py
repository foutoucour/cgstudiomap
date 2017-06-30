# -*- coding: utf-8 -*-
import logging

import simplejson
from datadog import statsd
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request, werkzeug

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def build_query(term, field, type_, table, where_condition=None):
    """

    :param str term:
    :param str field:
    :param str type_:
    :param str table:
    :param str|None where_condition:
    :return:
    """
    query_pattern = "SELECT {field} as data, {field}::text||' ({type_})' as label FROM {table}".format(
        field=field, type_=type_, table=table
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
        ('name', 'company', 'res_partner', "is_company is True AND state = 'open'"),
        ('name', 'country', 'res_country'),
        ('name', 'industry', 'res_industry'),
        ('name', 'state', 'res_country_state'),
        ('city', 'city', 'res_partner', 'is_company is True AND city is not null')
    )
    # Alphabetical order for the results
    query = '{0} ORDER BY label'.format(' UNION '.join(build_query(term, *case) for case in cases))
    logger.debug('query: %s', query)
    cr.execute(query)
    result = cr.dictfetchall()
    logger.debug('Result: %s', result)
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
        result = select_from_term(term) if term else []
        return simplejson.dumps(result)
