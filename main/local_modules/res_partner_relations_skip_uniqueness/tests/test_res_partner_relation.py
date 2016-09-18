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

from openerp.exceptions import ValidationError
from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartnerRelation(common.TransactionCase):
    """Test suites skip_uniqueness feature in res.partner.relation."""

    def setUp(self):
        """Overcharge the default setUp to expose the partner_relation_pool."""
        super(TestResPartnerRelation, self).setUp()
        self.partner_relation_type_pool = self.env['res.partner.relation.type']
        self.partner_relation_pool = self.env['res.partner.relation']
        self.partner_pool = self.env['res.partner']

    def test_multipleTimesTheSameRelation(self):
        """Check the system accepts multiple time the same relation if skip_uniqueness
        is True."""
        type_uniqueness_skiped = self.partner_relation_type_pool.create(
            {'name': 'multiple', 'name_inverse': 'elpitlum', 'skip_uniqueness': True}
        )
        partner1 = self.partner_pool.create({'name': 'partner1'})
        partner2 = self.partner_pool.create({'name': 'partner2'})
        self.partner_relation_pool.create(
            {
                'left_partner_id': partner1.id,
                'right_partner_id': partner2.id,
                'type_id': type_uniqueness_skiped.id
            }
        )
        self.partner_relation_pool.create(
            {
                'left_partner_id': partner1.id,
                'right_partner_id': partner2.id,
                'type_id': type_uniqueness_skiped.id
            }
        )

        self.assertEqual(2, partner1.relation_count)
