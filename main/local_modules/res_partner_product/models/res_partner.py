# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
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
import re
import logging
from openerp.osv import fields as osv_fields
from openerp import models, api, fields
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add relations with products."""
    _inherit = 'res.partner'
    product_user_ids = fields.Many2many(
        'product.template',
        'partner_user_rel',
        'part_id',
        'prod_id',
        'Softwares Used'
    )
    product_developer_ids = fields.Many2many(
        'product.template',
        'partner_developer_rel',
        'part_id',
        'prod_id',
        'Softwares Developed'
    )

class ProductTemplate(models.Model):
    """Add relations with products."""
    _inherit = 'product.template'
    is_company_domain = [('is_company', '=', True)]

    partner_user_ids = fields.Many2many(
        'res.partner',
        'partner_user_rel',
        'prod_id',
        'part_id',
        'Used by:',
        domain=is_company_domain,
        help='Companies using the product.'
    )

    partner_developer_ids = fields.Many2many(
        'res.partner',
        'partner_developer_rel',
        'prod_id',
        'part_id',
        'Developed by:',
        domain=is_company_domain,
        help='Companies working to develop the product.'
    )

    def _partner_user_count(self, cr, uid, ids, field_name, arg, context=None):
        """Return the number of partner using the product."""
        return self.__partner_count(
            cr, uid, ids, 'product_user_ids', arg, context=context
        )

    def _partner_developer_count(self, cr, uid, ids, field_name, arg, context=None):
        """Return the numbe of partner developing the product."""
        return self.__partner_count(
            cr, uid, ids, 'product_developer_ids', arg, context=context
        )

    # Using old api to avoid the high number of write the new api seems to cost.
    _columns = {
        'partner_user_count': osv_fields.function(
            _partner_user_count, string='# Users', type='integer'
        ),
        'partner_developer_count': osv_fields.function(
            _partner_developer_count, string='# Developers', type='integer'
        ),
    }

    def action_partner_user(self, cr, uid, ids, context=None):
        """Show the view of partner with all the partners using the product."""
        return self.__get_action_partner(
            cr, uid, ids, 'product_user_ids', context
        )

    def action_partner_developer(self, cr, uid, ids, context=None):
        """Show the view of partner with all the partners developing the
        product.
        """
        return self.__get_action_partner(
            cr, uid, ids, 'product_developer_ids', context
        )

    def __get_action_partner(self, cr, uid, ids, field_name, context=None):
        result = self.pool['ir.model.data'].xmlid_to_res_id(
            cr, uid, 'portal_user.action_portal_companies',
            raise_if_not_found=True
        )
        result = self.pool['ir.actions.act_window'].read(
            cr, uid, [result], context=context
        )[0]
        result['domain'] = ''.join([
            "[('{0}','in',[".format(field_name),
            ','.join(map(str, ids)),
            "])]"
        ])
        return result

    def __partner_count(self, cr, uid, ids, field_name, arg, context=None):
        id_ = ids[0]
        partner_pool = self.pool['res.partner']
        domain = [
            (field_name, '=', id_)
        ]
        return {id_: partner_pool.search_count(cr, uid, domain, context=context)}
