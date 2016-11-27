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

import mock
from openerp.tests import common
import openerp.addons.res_partner_moderator_supervision.res_partner as rp

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites interaction between the create and update and the slack logger."""
    module_name = 'openerp.addons.res_partner_moderator_supervision.res_partner'
    path_main_slack_logger = '{0}.main_slack_logger'.format(module_name)
    path_conditions_for_logging ='{0}.ResPartner.conditions_for_logging'.format(
        module_name
    )

    def setUp(self):
        """Overcharge the default setUp to expose the partner_pool."""
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.klass = rp.ResPartner

    @mock.patch(path_main_slack_logger)
    @mock.patch(path_conditions_for_logging, return_value=False)
    def test_create_noValidConditions(self, mock_condition_for_logging, mock_log):
        """Check that log is emit if the condition of logging are not met
        during a create of a partner.
        """
        del mock_condition_for_logging
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        self.assertEqual(0, mock_log.info.call_count)

    @mock.patch(path_main_slack_logger)
    @mock.patch(path_conditions_for_logging, return_value=True)
    def test_create_validConditions(self, mock_condition_for_logging, mock_log):
        """Check that log is emit if the condition of logging are met."""
        del mock_condition_for_logging
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        self.assertEqual(1, mock_log.info.call_count)

    @mock.patch(path_main_slack_logger)
    @mock.patch(path_conditions_for_logging, return_value=False)
    def test_update_noValidCondition(self, mock_condition_for_logging, mock_log):
        """Check that log is emit if the condition of logging are not met
        during an update of a partner.
        """
        del mock_condition_for_logging
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        partner.write({'name': 'tupdate'})
        self.assertEqual('tupdate', partner.name)
        self.assertEqual(0, mock_log.info.call_count)

    @mock.patch(path_main_slack_logger)
    @mock.patch(path_conditions_for_logging, return_value=True)
    def test_update_validCondition(self, mock_condition_for_logging, mock_log):
        """Check that log is emit if the condition of logging are met
        during an update of a partner.
        """
        del mock_condition_for_logging
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        partner.write({'name': 'tupdate'})
        self.assertEqual('tupdate', partner.name)
        self.assertEqual(2, mock_log.info.call_count)

    @mock.patch('{0}.ResUsers.is_contributor'.format(module_name), return_value=True)
    @mock.patch(path_main_slack_logger)
    @mock.patch(path_conditions_for_logging, return_value=True)
    def test_update_doneByContributor(self,
                                      mock_condition_for_logging,
                                      mock_log,
                                      mock_is_contributor):
        """Check that log is emit by the secondary slack logger if the update is done
        by a partner part of the contributor group.

        Because of the high number of updates we are facing, it turned to be hard to
        know what should be moderated. We want to silence the updates done by moderators
        as the updates are mostly due to the moderation itself.
        """
        del mock_condition_for_logging, mock_is_contributor
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        partner.write({'name': 'tupdate'})
        self.assertEqual('tupdate', partner.name)
        # Only one call, for the creation, as the update done by a contributor should
        # not trigger the emit.
        self.assertEqual(1, mock_log.info.call_count)

    @mock.patch(path_main_slack_logger, True)
    def test_condition_for_logging(self):
        """Check the behavior of the function when there all conditions are met."""
        user = mock.MagicMock(name='mock_user')
        user.id = 4
        partner = mock.MagicMock(name='mock_partner')
        partner.is_company = True
        self.assertIs(True, self.klass.conditions_for_logging(user, partner))

    @mock.patch(path_main_slack_logger, False)
    def test_condition_for_logging_noSlackLogger(self):
        """Check the behavior of the function when there is no slack logger."""
        user = mock.MagicMock(name='mock_user')
        user.id = 4
        partner = mock.MagicMock(name='mock_partner')
        partner.is_company = True
        self.assertIs(
            False, self.klass.conditions_for_logging(user, partner),
            msg='Condition validated even without logger.'
        )

    @mock.patch(path_main_slack_logger, True)
    def test_condition_for_logging_notCompany(self):
        """Check the behavior of the function when there is a slack logger."""
        user = mock.MagicMock(name='mock_user')
        user.id = 4
        partner = mock.MagicMock(name='mock_partner')
        partner.is_company = False
        self.assertIs(
            False, self.klass.conditions_for_logging(user, partner),
            msg='Condition validated even with the partner that is not a company.'
        )

    @mock.patch(path_main_slack_logger, True)
    def test_condition_for_logging_admin(self):
        """Check the behavior of the function when the user that does the update
        is the admin (id = 1)."""
        user = mock.MagicMock(name='mock_user')
        user.id = 1
        partner = mock.MagicMock(name='mock_partner')
        partner.is_company = True
        self.assertIs(
            False, self.klass.conditions_for_logging(user, partner),
            msg='Condition validated even with user as admin.'
        )

    @mock.patch(path_main_slack_logger, True)
    def test_condition_for_logging_publicUser(self):
        """Check the behavior of the function when the user that does the update
        is the public user (id = 3)."""
        user = mock.MagicMock(name='mock_user')
        user.id = 3
        partner = mock.MagicMock(name='mock_partner')
        partner.is_company = True
        self.assertIs(
            False, self.klass.conditions_for_logging(user, partner),
            msg='Condition validated even with user as public user.'
        )
