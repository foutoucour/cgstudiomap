# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
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

    # query used to
    map_query = """
    SELECT
      rp.id,
      rp.partner_latitude,
      rp.partner_longitude,
      rp.name,
      rp.id,
      rp.city as city_name,
      res_country_state.name as state_name,
      res_country.name as country_name,
      ind.name as ind_name
    FROM res_partner as rp
    INNER JOIN res_country_state
      ON rp.state_id=res_country_state.id
    INNER JOIN res_country
      ON rp.country_id=res_country.id
    INNER JOIN res_industry_res_partner_rel AS rpr
      ON rpr.res_partner_id = rp.id
    INNER JOIN res_industry as ind
      ON ind.id = rpr.res_industry_id
    WHERE
      rp.id IN ({})
    """

    def get_map_partners_dict(self, ids):
        """Get a dict with the details of the partners of the given ids.

        :param list ids: list of ints
        :rtype: dict
        :return: details of the partners.
        """
        cr = self.env.cr
        cr.execute(self.map_query.format(','.join(str(id_) for id_ in ids)))
        return cr.dictfetchall()
