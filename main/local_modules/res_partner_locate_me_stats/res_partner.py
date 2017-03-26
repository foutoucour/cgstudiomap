# -*- encoding: utf-8 -*-

import logging
import datetime
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class ResPartnerLocateMeStats(models.Model):
    """Represent the Usage Of The Feature Locate Me."""
    _name = 'res.partner.locate_me_stats'
    _description = __doc__

    user_id = fields.Many2one('res.partner', string='User')
    latitude = fields.Float('Latitude', digits=(16, 5))
    Longitude = fields.Float('Longitude', digits=(16, 5))
    success = fields.Boolean('Geo location successed?')


class ResPartner(models.Model):
    """Add a method to add a Locate Me Stats."""
    _inherit = 'res.partner'

    @api.model
    def add_locate_me_view(self, success, latitude=None, longitude=None):
        """Add an entry res.partner.count.view.

        :param bool success: True if the geo-location successed.
        :param float|None latitude: latitude of the geo location. Default: None
        :param float|None longitude: longitude of the geo location. Default: None
        :return: the new res.partner.locate_me_stats entry.
        """
        locate_me_stats = self.env['res.partner.locate_me_stats']
        details = {
            'user': self.id,
            'success': success
        }
        if longitude and latitude:
            details.update({
                'latitude': latitude,
                'longitude': longitude,
            })

        return locate_me_stats.create(details)
