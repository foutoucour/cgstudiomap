# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)
from openerp.addons.frontend_listing.controllers.listing import Listing

from openerp import http
from openerp.exceptions import ValidationError, except_orm
from openerp.http import request

_logger = logging.getLogger(__name__)


class About(Base):
    """Representation of the page About of the website."""

    @statsd.timed('odoo.frontend.about.time')
    @http.route('/aboutus', type='http', auth="public", website=True)
    def about(self):
        """Render the page of About.

        :return: request.render
        """
        env = request.env
        partner_pool = env['res.partner']
        values = {
            'partners': partner_pool.get_contributors()
        }
        return request.website.render('frontend_about.aboutus', values)
        # return request.website.render('frontend_about.view', values)

