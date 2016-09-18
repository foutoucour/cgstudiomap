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

import os
import logging
import socket
import getpass

from slack_log_handler import SlackLogHandler

from openerp import models, api

_logger = logging.getLogger(__name__)

# see https://cgstudiomap.slack.com/apps/manage/A0F7XDUAZ-incoming-webhooks
# for the url.
# Use test_hook url webhook for tests
WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_MODERATION', '')
_logger.debug('WEBHOOK_URL: %s', WEBHOOK_URL)



def get_slack_logger(name, hook):
    """Build a `logging.logger` instance with a special handler that will
    send a notification to cgstudiomap slack.

    :param str name: name of the logger.
    :param str hook: url of the hook to use to send the notification.

    :return: logging.logger instance.
    """
    slack_handler = SlackLogHandler(hook, username='Jazz')
    slack_handler.formatter = logging.Formatter(
        "%(asctime)s GMT - %(message)s", "%Y-%m-%d %H:%M"
    )
    slack_handler.setLevel(logging.INFO)
    slack_handler.EMOJIS[logging.INFO] = ':jazz:'
    slack_handler.EMOJIS[logging.NOTSET] = ':jazz:'
    slack_handler.EMOJIS[logging.WARNING] = ':jazz:'
    slack_handler.EMOJIS[logging.ERROR] = ':jazz:'
    slack_logger = logging.getLogger(name)
    slack_logger.addHandler(slack_handler)
    slack_logger.info(
        'Jazz Ready for action! (From: {0}@{1})'.format(
            getpass.getuser(), socket.gethostname(),
        )

    )
    return slack_logger


if WEBHOOK_URL:
    _slack_logger = get_slack_logger(__name__, WEBHOOK_URL)
else:
    _logger.warning('No value for SLACK_WEBHOOK_MODERATION. No moderation.')
    _slack_logger = None


class ResPartner(models.Model):
    """Represent addition of slack notification for updates and creation of
    records of the model.
    """
    _inherit = 'res.partner'

    @staticmethod
    def conditions_for_logging(user, partner):
        """Check if all the conditions are set to log the message of moderation

        :param record user: user that did the update.
        :param record partner: the partner updated.
        :rtype: bool
        """
        # id > 3 so admin, template and public actions are not logged
        # we only care about updated companies, not about people.
        return _slack_logger and user.id > 3 and partner.is_company

    @api.multi
    def write(self, vals):
        """Overcharge to add notification to slack."""
        ret = super(ResPartner, self).write(vals)
        user = self.env['res.users'].browse(self._uid)
        if self.conditions_for_logging(user, self):
            message = ''.join([
                '<http://www.cgstudiomap.org%s|%s> '
                '(id: %s) has been *updated*. ',
                'Update done by %s (id: %s).'
            ])
            _slack_logger.info(
                message,
                self.partner_url,
                self.name.encode('utf8'),
                str(self.id),
                user.login,
                str(user.id)
            )

        return ret

    @api.model
    def create(self, vals):
        """Overcharge to add notification to slack."""
        ret = super(ResPartner, self).create(vals)
        user = self.env['res.users'].browse(self._uid)
        if self.conditions_for_logging(user, ret):
            message = '. '.join([
                'A new company has been *added*: '
                '<http://www.cgstudiomap.org%s|%s> '
                '(id: %s). ',
                'Update done by %s (id: %s).'
            ])

            _slack_logger.info(
                message,
                ret.partner_url,
                ret.name.encode('utf8'),
                str(ret.id),
                user.login,
                str(user.id)
            )

        return ret
