# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging

from openerp import api, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_contributors(self):
        """Return all the partners that are considered as contributors.

        :return: list of partner that match the criteria of contributors
        """
        ir_model_data = self.env['ir.model.data']
        contributor_group = ir_model_data.xmlid_to_object(
            'res_group_archetype.group_archetype_contributor'
        )
        user_pool = self.env['res.users']
        user_contributors = user_pool.search([('groups_id', 'in', contributor_group.id)])
        return [user.partner_id for user in user_contributors]
