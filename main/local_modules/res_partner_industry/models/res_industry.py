# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
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
from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class ResIndustryFamily(models.Model):
    _name = 'res.industry.family'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Group of Industries'

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=4)
    image = fields.Binary(
        "Image",
        help="This field holds the image used as avatar for this family,"
             " limited to 1024x1024px"
    )
    description = fields.Text('Description')


class ResIndustry(models.Model):
    _name = 'res.industry'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Industry'

    name = fields.Char('Name', size=128, required=True)
    family_ids = fields.Many2many(
        'res.industry.family',
        string='Industry Families',
    )
    image = fields.Binary(
        "Image",
        help="This field holds the image used as avatar for this industry,"
             " limited to 1024x1024px"
    )
    description = fields.Text('Description')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    industry_family_ids = fields.Many2many(
        'res.industry.family',
        string='Industry Families',
        )

    industry_ids = fields.Many2many(
        'res.industry',
        string='Industries',
    )

    @api.model
    def _get_industry_details_from_context(self, vals):
        """Find the industries mentionned in the context"""
        _logger.debug('context: {}'.format(self._context))
        industry_family_codes = self._context.get('industry_family_codes', [])
        _logger.debug(
            'industry_family_codes: {}'.format(industry_family_codes)
        )

        if industry_family_codes:
            _logger.debug('industry_family_codes: True')
            industry_family_pool = self.env['res.industry.family']
            vals['industry_family_ids'] = [
                (4, family.id) for family in industry_family_pool.search([
                    ('code', 'in', industry_family_codes)
                ])
            ]
            _logger.debug(
                'vals[industry_family_ids]: {}'.format(
                    vals['industry_family_ids']
                )
            )
        return vals

    @api.multi
    def write(self, vals):
        return super(ResPartner, self).write(
            self._get_industry_details_from_context(vals)
        )

    @api.model
    def create(self, vals):
        return super(ResPartner, self).create(
            self._get_industry_details_from_context(vals)
        )
