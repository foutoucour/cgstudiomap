# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging
import random

from caches import clear_caches
from openerp import api, models, fields

_logger = logging.getLogger(__name__)


class ResIndustry(models.Model):
    _inherit = 'res.industry'

    tag_url = fields.Char('Tag Url', compute='industry_tag_url_link')

    @api.one
    def industry_tag_url_link(self):
        self.tag_url = (
            '<a itemprop="name" href="/directory?search={0.name}">'
            '<span class="label label-info">{0.name}</span></a>'.format(self)
        )
        # self.tag_url = '<span class="label label-info">{0.name}</span>'.format(
        #     self
        # )
