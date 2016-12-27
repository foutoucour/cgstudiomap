# -*- coding: utf-8 -*-
"""Definition for website constants."""
import logging

from openerp import models, fields

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    directory_menu = '/directory'
    shop_menu = '/shop/'
    about_menu = '/contactus/'
