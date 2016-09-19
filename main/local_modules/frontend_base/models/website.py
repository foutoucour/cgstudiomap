# -*- coding: utf-8 -*-
"""Definition for website and website.iframe.host."""
import logging

from openerp import models, fields

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    directory_menu = '/directory'
    shop_menu = '/shop/'
    about_menu = '/contactus/'


class WebsiteIframeHost(models.Model):
    """Represent the name of a host that can embed our listing."""
    _name = 'website.iframe.host'
    _description = _name

    host = fields.Char('Host', help='Name of the the host that will embed the listing.')
    search_domain = fields.Char(
        'Search Domain',
        help='Domain that will be injected in searches for the given host.'
    )
