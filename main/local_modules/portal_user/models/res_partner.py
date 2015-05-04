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
import pprint
from openerp import fields, models, api

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _is_portal_user(self):
        """Check if the current user is a portal user.

        This hack allows to set a sort of context to the view.
        """
        user = self.env['res.users'].browse(self._uid)
        portal_group = self.env['ir.model.data'].get_object('base',
                                                            'group_portal')
        ret = portal_group in user.groups_id
        _logger.debug('_is_portal_user (uid = {}): {}'.format(self._uid, ret))
        return ret

    @api.model
    def create(self, vals):
        """Set True to is_company if the res.partner is created by someone using
        the portal."""
        vals['is_company'] = self._is_portal_user()
        _logger.debug('vals: {}'.format(pprint.pformat(vals)))
        return super(ResPartner, self).create(vals)

    # Constant to test against to see if the current user is a portal user
    # Should be used in couple with context
    is_portal_user = fields.Boolean(default=True)

    @api.one
    def _is_favorite(self):
        """Check to know if the res.partner is a favorite of the user."""
        self.favorite = self.env['res.users'].browse(self._uid) in self.favorite_ids

    @api.one
    def _set_favorite(self):
        """Set or unset the res.partner as a favorite of the user.

        Check the statuts of favorite field to know if the user wants to
        set or unset the record as partner. It adds or remove the user
        from favorite_ids according to the setting.
        """
        user = self.env['res.users'].browse(self._uid)
        if self.favorite:
            code = 4
        else:
            code = 3
        return self.write({'favorite_ids': [(code, user.id)]})

    # List of users that favorited the res.partner.
    favorite_ids = fields.Many2many('res.users', string='favorited by')
    # To note if a company is a favorite of the user.
    # The field is set dynamically. It exists only to help the user experience.
    favorite = fields.Boolean(
        'Favorite', default=False, inverse=_set_favorite, compute=_is_favorite,
        help='Set the company as one of your favorites.'
    )

