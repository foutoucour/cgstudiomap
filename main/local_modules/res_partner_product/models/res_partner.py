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

    def _product_user_count(self, cr, uid, ids, field_name, arg, context=None):
        """Return the number of partner using the product."""
        id_ = ids[0]
        partner_pool = self.pool['product.template']
        domain = [
            ('partner_user_ids', '=', id_)
        ]
        return {id_: partner_pool.search_count(cr, uid, domain, context=context)}

    def _product_brand_count(self, cr, uid, ids, field_name, arg, context=None):
        """Return the number of partner using the product."""
        id_ = ids[0]
        partner_pool = self.pool['product.brand']
        domain = [
            ('partner_id', '=', id_)
        ]
        return {id_: partner_pool.search_count(cr, uid, domain, context=context)}

    # Using old api to avoid the high number of write the new api seems to cost.
    _columns = {
        'product_user_count': osv_fields.function(
            _product_user_count, string='Softwares', type='integer'
        ),
        'product_brand_count': osv_fields.function(
            _product_brand_count, string='Brands', type='integer'
        ),
    }

    def action_product_user(self, cr, uid, ids, context=None):
        """Show the view of partner with all the partners using the product."""
        result = self.pool['ir.model.data'].xmlid_to_res_id(
            cr, uid, 'portal_user.action_portal_software',
            raise_if_not_found=True
        )
        result = self.pool['ir.actions.act_window'].read(
            cr, uid, [result], context=context
        )[0]
        result['domain'] = ''.join([
            "[('partner_user_ids','in',[",
            ','.join(map(str, ids)),
            "])]"
        ])
        return result

    def action_product_brand(self, cr, uid, ids, context=None):
        """Show the view of partner with all the partners using the product."""
        result = self.pool['ir.model.data'].xmlid_to_res_id(
            cr, uid, 'portal_user.action_portal_product_brand',
            raise_if_not_found=True
        )
        result = self.pool['ir.actions.act_window'].read(
            cr, uid, [result], context=context
        )[0]
        result['domain'] = ''.join([
            "[('partner_id','in',[",
            ','.join(map(str, ids)),
            "])]"
        ])
        return result

class ProductTemplate(models.Model):
    """Add relations with products."""
    _inherit = 'product.template'

    partner_user_ids = fields.Many2many(
        'res.partner',
        'partner_user_rel',
        'prod_id',
        'part_id',
        'Used by:',
        domain=[('is_company', '=', True)],
        help='Companies using the product.'
    )

    def _partner_user_count(self, cr, uid, ids, field_name, arg, context=None):
        """Return the number of partner using the product."""
        id_ = ids[0]
        partner_pool = self.pool['res.partner']
        domain = [
            ('product_user_ids', '=', id_)
        ]
        return {id_: partner_pool.search_count(cr, uid, domain, context=context)}

    # Using old api to avoid the high number of write the new api seems to cost.
    _columns = {
        'partner_user_count': osv_fields.function(
            _partner_user_count, string='# Users', type='integer'
        ),
    }

    def action_partner_user(self, cr, uid, ids, context=None):
        """Show the view of partner with all the partners using the product."""
        result = self.pool['ir.model.data'].xmlid_to_res_id(
            cr, uid, 'portal_user.action_portal_companies',
            raise_if_not_found=True
        )
        result = self.pool['ir.actions.act_window'].read(
            cr, uid, [result], context=context
        )[0]
        result['domain'] = ''.join([
            "[('product_user_ids','in',[",
            ','.join(map(str, ids)),
            "])]"
        ])
        return result


class ProductBrand(models.Model):
    """Partner only can be a company."""
    _inherit = 'product.brand'

    partner_id = fields.Many2one(domain=[('is_company', '=', True)])

