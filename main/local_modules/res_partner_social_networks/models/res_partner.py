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
import logging
import re

from openerp import models, api, fields
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add Social Networks fields."""
    _inherit = 'res.partner'

    twitter = fields.Char('Twitter')
    youtube = fields.Char('Youtube')
    vimeo = fields.Char('Vimeo')

    linkedin = fields.Char('Linkedin')
    facebook = fields.Char('Facebook')
    wikipedia = fields.Char('Wikipedia')
    github = fields.Char('Github')

    _twitter_regex = r'https?://(www\.)?twitter\.com/\w+'
    _twitter_error_message = _(
        'The entry for Twitter seems not to be correct.'
        '\nA twitter account should be something '
        'like https://www.twitter.com/cgstudiomap'
    )
    _linkedin_regex = r'https?://(www\.)?linkedin\.com/company/[\w-]+'
    _linkedin_error_message = _(
        'The entry for LinkedIn seems not to be correct.'
        '\nA linkedin account should be something '
        'like https://www.linkedin.com/company/cgstudiomap.com'
    )
    _facebook_regex = r'https?://(www\.)?facebook\.com/[\w-]+'
    _facebook_error_message = _(
        'The entry for Facebook seems not to be correct.'
        '\nA facebook account should be something '
        'like https://www.facebook.com/ followed the name of the company.'
    )
    _youtube_regex = r'https?://(www\.)?youtube\.com/'
    _youtube_error_message = _(
        'The entry for Youtube seems not to be correct.'
        '\nA youtube account should start by '
        'https://www.youtube.com/ followed by the account name.'
    )
    _vimeo_regex = r'https?://(www\.)?vimeo\.com/'
    _vimeo_error_message = _(
        'The entry for Vimeo seems not to be correct.'
        '\nA vimeo account should start by '
        'https://www.vimeo.com followed by the account name.'
    )
    _github_regex = r'https?://(www\.)?github\.com/\w+'
    _github_error_message = _(
        'The entry for Github seems not to be correct.'
        '\nA twitter account should be something '
        'like https://www.github.com/cgstudiomap'
    )


    @api.model
    def _validate_social_network_url(self, url, regex, err_msg):
        _logger.debug('_validate_social_network_url')
        _logger.debug('url: {}'.format(url))
        _logger.debug('regex: {}'.format(regex))
        self._url_validation(url)
        if not re.match(regex, url):
            err_msg = _(
                'The given url ("{}") seems not to be an account.'.format(url)
            )
            raise ValidationError(err_msg)

    @property
    def _url_fields(self):
        """Add social networks fields to inital list of url fields."""
        fields = super(ResPartner, self)._url_fields
        fields.extend([
            'twitter', 'youtube', 'vimeo', 'facebook', 'linkedin',
            # 'wikipedia', 'art_of_fx',
        ])
        return fields

    @api.one
    @api.constrains('twitter')
    def _validate_twitter_url_constrains(self):
        """Add a constrains to the twitter field."""
        self._validate_twitter_url(self.twitter)

    @classmethod
    def _validate_twitter_url(cls, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = cls.__strip_value(value)
        regex = cls._twitter_regex
        if url:
            cls._url_validation(url)
            if not re.match(regex, url):
                err_msg = cls._twitter_error_message
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('linkedin')
    def _validate_linkedin_url_constrains(self):
        """Add a constrains to the linkedin field."""
        self._validate_linkedin_url(self.linkedin)

    @classmethod
    def _validate_linkedin_url(cls, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = cls.__strip_value(value)
        # Linkedin got its page tracking system embed in the url
        # then the url can be followed by ?trk...
        regex = cls._linkedin_regex
        if url:
            cls._url_validation(url)
            if not re.match(regex, url):
                err_msg = cls._linkedin_error_message
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('facebook')
    def _validate_facebook_url(self):
        """Add a constrains to the facebook field."""
        self._validate_facebook_url(self.facebook)

    @classmethod
    def _validate_facebook_url(cls, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = cls.__strip_value(value)
        # Facebook got its page tracking system embed in the url
        # then the url can be followed by ?fref...
        regex = cls._facebook_regex
        if url:
            cls._url_validation(url)
            if not re.match(regex, url):
                err_msg = cls._facebook_error_message
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('youtube')
    def _validate_youtube_url_constrains(self):
        """Add a constrains to the youtube field."""
        self._validate_youtube_url(self.youtube)

    @classmethod
    def _validate_youtube_url(cls, value):
        """Check the youtube url.

        :param str value: url to check. Can be False.
        """
        url = cls.__strip_value(value)
        regex = cls._youtube_regex
        if url:
            cls._url_validation(url)
            if not re.match(regex, url):
                err_msg = cls._youtube_error_message
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('vimeo')
    def _validate_vimeo_url_constrains(self):
        """Add a constrains to the vimeo field."""
        self._validate_vimeo_url(self.vimeo)

    @classmethod
    def _validate_vimeo_url(cls, value):
        """Check the vimeo url.

        :param str value: url to check. Can be False.
        """
        url = cls.__strip_value(value)
        regex = cls._vimeo_regex
        if url:
            cls._url_validation(url)
            if not re.match(regex, url):
                err_msg = cls._vimeo_error_message
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('github')
    def _validate_github_url_constrains(self):
        """Add a constrains to the github field."""
        self._validate_github_url(self.github)

    @classmethod
    def _validate_github_url(cls, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = cls.__strip_value(value)
        regex = cls._github_regex
        if url:
            cls._url_validation(url)
            if not re.match(regex, url):
                err_msg = cls._github_error_message
                raise ValidationError(err_msg)

    @staticmethod
    def __strip_value(value):
        """strip if the value is a string.

        :param object value: value to attempt to strip.
        :return: striped value.
        """
        if isinstance(value, basestring):
            return value.strip()

        return value
