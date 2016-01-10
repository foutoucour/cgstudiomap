# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging
import random

from caches import clear_caches
from openerp import api, models, fields

_logger = logging.getLogger(__name__)


class ResIndustry(models.Model):
    _inherit = 'res.industry'

    def tag_url_link(self,
                     company_status='open',
                     listing=False):
        url = '/directory'
        url += listing and '/list' or ''
        url += '?company_status={0}'.format(company_status)
        url += '&search={0}'.format(self.name)

        return (
            '<a itemprop="name" href="{1}">'
            '<span class="label label-info">{0.name}</span></a>'.format(
                self, url
            )
        )
