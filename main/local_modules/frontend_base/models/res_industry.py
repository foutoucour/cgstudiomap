# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging

from openerp import  models

_logger = logging.getLogger(__name__)


class ResIndustry(models.Model):
    _inherit = 'res.industry'

    def tag_url_link(self,
                     company_status='open',
                     listing=False):
        """build the tag of an industry from an indutry record.

        For more details see tag_url_link_details.
        """
        return self.tag_url_link_details(self.name, company_status, listing)

    @staticmethod
    def tag_url_link_details(ind_name,
                             company_status='open',
                             listing=False
                             ):
        """Build the tag of an industry from the given name.

        :param str ind_name: name of the industry the tag is related to.
        :param str company_status: status of the search related to the tag
        :param bool listing: if the tag should point to the list (True). Default: False.
        :return: html  code to build the tag.
        :rtype: str
        """
        url = listing and '/directorylist' or ''
        url += '?company_status={0}'.format(company_status)
        url += '&search={0}'.format(ind_name)

        return (
            '<a itemprop="name" href="{1}">'
            '<span class="label label-info">{0}</span></a>'.format(
                ind_name, url
            )
        )
