# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.users."""
import logging

from openerp import models

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    directory_menu = '/directory'
    shop_menu = '/shop/'
    about_menu = '/page/website.contactus'
