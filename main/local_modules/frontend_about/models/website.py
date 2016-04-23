# -*- coding: utf-8 -*-
"""Suite of methods common operation on website."""
import logging

from openerp import models

_logger = logging.getLogger(__name__)


class Website(models.Model):
    """Redefine the url used for the about page."""
    _inherit = 'website'

    about_menu = '/aboutus'
