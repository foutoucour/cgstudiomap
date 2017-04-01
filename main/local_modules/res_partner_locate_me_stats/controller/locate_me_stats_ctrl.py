# -*- coding: utf-8 -*-
import simplejson
from datadog import statsd
from openerp.http import request
from openerp.addons.web import http
from openerp.addons.frontend_base.controllers.base import Base


class LocateMeStats(Base):
    """Representation of ajax route for locate_me workflow."""

    # Will allow to track the number of use in datadog. Easier than in odoo.
    @statsd.timed('odoo.backend.ajax.locate_me_stats', tags=['backend', 'backend:locate_me_stats', 'ajax'])
    @http.route('/ajax/locate_me_stats', type='http', auth="public", methods=['POST'])
    def locate_me_stats(self, success, latitude=None, longitude=None):
        """Add an entry in the database to track a usage of locate me

        :param bool success: if the locate me succeeded or not
        :param float|None latitude: latitude of the geo-location
        :param float|None longitude: longitude of the geo-location
        :return:
        """
        user_partner = request.env['res.users'].browse(request.uid).partner_id
        user_partner.add_locate_me_view(success, latitude=latitude, longitude=longitude)
        return simplejson.dumps({})
