# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import datetime
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class ResPartnerCountView(models.Model):
    """Represent the visit from a partner to a company page."""
    _name = 'res.partner.count.view'
    _description = __doc__

    active_partner_id = fields.Many2one('res.partner', string='Viewer')
    passive_partner_id = fields.Many2one('res.partner', string='Viewed')
    ip = fields.Char('IP of the viewer')
    host = fields.Char('Host the viewer used')


class ResPartner(models.Model):
    """Add a method to add a count."""
    _inherit = 'res.partner'

    @api.model
    def add_count_view(self, viewed_partner, request):
        """Add an entry res.partner.count.view.

        :param viewed_partner: The visited partner.
        :param werkzeug.local.LocalStack request: request the view has been done with.
        :return: the new res.partner.count.view entry.
        """
        counter_pool = self.env['res.partner.count.view']
        return counter_pool.create({
            'active_partner_id': self.id,
            'passive_partner_id': viewed_partner.id,
            'ip': request.httprequest.remote_addr,
            'host': request.httprequest.host,
        })
