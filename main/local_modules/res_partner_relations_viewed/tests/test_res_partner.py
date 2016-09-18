# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
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

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites skip_uniqueness feature in res.partner.relation."""

    def setUp(self):
        """Overcharge the default setUp to expose the partner_relation_pool."""
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

    def test_add_viewedby_relation(self):
        """Check the method creates the relation viewed between the partners."""
        viewed_relation_type = self.env['ir.model.data'].get_object(
            'res_partner_relations_viewed', 'rel_type_viewed'
        )
        partner_company = self.partner_pool.create(
            {'name': 'company', 'is_company': True}
        )
        partner = self.partner_pool.create(
            {'name': 'person'}
        )
        partner_company.add_viewed_by_relation(partner)
        relations = partner.relation_ids

        self.assertEqual(1, len(relations))
        relation = relations[0]
        self.assertEqual(
            viewed_relation_type, relation.type_id,
            msg="The type of the relation is not a viewed/viewed_by"
        )
        today = str(datetime.date.today())
        self.assertEqual(today, relation.date_start)
        self.assertEqual(today, relation.date_end)
