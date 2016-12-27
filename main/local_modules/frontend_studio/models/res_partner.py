# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import base64
import logging
import pprint
import random

from openerp import api, models, fields

_logger = logging.getLogger(__name__)


class ResPartnerGetStudios(models.Model):
    """Overcharge the definition of a partner with methods to get studios
    from the location of the partner.
    """
    _inherit = 'res.partner'
    visit_count = fields.Integer(
        'Number of visit for this partner',
        readonly=True,
        help='Number increased each time the frontend  page of the studio is opened.'
    )

    @api.model
    def get_studios_from_same_location(self):
        """Return a list of partners that have a logo with the same locations
        that the given partner.

        :return: list of partner records.
        """
        company_pool = self.env['res.company']
        # #294
        # Looking for cgstudiomap to avoid to have it displayed.
        # cgstudiomap is actually the partner linked to the res.company
        # of the instance.
        # looking for the first (and only so far) res.company
        company = company_pool.browse(1)

        # https://github.com/cgstudiomap/cgstudiomap/issues/177
        # search return a recordset and we cannot do len() on it.
        partners = [
            partner for partner in self.search(
                self.open_companies_domain.search +
                [
                    ('id', '!=', company.partner_id.id),
                    ('image', '!=', False),
                    ('country_id', '=', self.country_id.id),
                    ('id', '!=', self.id)
                ]
            )
            ]

        return partners

    @api.model
    def get_random_studios_from_same_location(self, sample_):
        """Return a random sample from the list of partners
        are returned from `self.get_studios_from_same_location`

        :param int sample_: size of the sample of partners.
        :return: list of partner records.
        """
        partners = self.get_studios_from_same_location()
        return random.sample(partners, min(len(partners), sample_))


class ResPartnerSave(models.Model):
    """Overcharge the definition of a partner to add methods to update
    from the save page.
    """
    _inherit = 'res.partner'

    @staticmethod
    def get_base64_from_filestore(filestore):
        """Encode a werkzerg.Filestore to a string using base64.

        :param werkzerg.Filestore filestore: instance that represents the
            new image of the partner.
        :return: image encoded using base64
        :rtype: str
        """
        return base64.b64encode(filestore.read())

    @api.model
    def clean_values_from_post_request(self,
                                       country_id=None,
                                       remove_image=False,
                                       image_file=None,
                                       **kwargs):
        """Clean the different values coming from the save post request.

        Data might be converted to be ingested by odoo.
        For example, list of industries has to be gathered from all the keys
        starting by industry_ids and converted into an odoo leaf to be ingested
        into the X2X industry_ids field.

        For the image several options to the user:
         - a bool (remove_image) that will just remove the current image.
         - a browse (image_file) that will replace the current image by the
         newly selected.

        If the remove_image is True, the image_file is ignored.

        :param int country_id: id of the country to set the partner to.
        :param bool remove_image: if the current image of the partner should
            be removed.
        :param werkzerg.Filestore image_file: instance that represents the
            new image of the partner.
        :param dict kwargs: list of additional fields to update.

        :return: request.render
        """
        values = kwargs
        if country_id:
            values['country_id'] = int(country_id)

        if remove_image:
            values['image'] = None

        _logger.debug('condition: %s', image_file and not remove_image)
        if image_file and not remove_image:
            values['image'] = self.get_base64_from_filestore(image_file)
        industry_ids = []
        for key, value in kwargs.items():
            if 'industry_ids' in key:
                industry_ids.append(int(value))
                del kwargs[key]

        if industry_ids:
            values['industry_ids'] = [(6, 0, industry_ids)]

        return values

    @api.model
    def create_from_post_request(self, kwargs):
        """Process a create from data coming from a post request."""
        values = self.clean_values_from_post_request(**kwargs)
        # Users are only allowed to create companies.
        values['is_company'] = True
        return self.create(values)

    @api.model
    def write_from_post_request(self, kwargs):
        """Process a write from data coming from a post request."""
        return self.write(self.clean_values_from_post_request(**kwargs))

    @api.one
    def full_location_studio_page(self):
        """Return the address as oneliner."""
        elements = []
        if self.street: elements.append(self.street)
        if self.street2: elements.append(self.street2)
        if self.city: elements.append(self.city)
        if self.zip: elements.append(self.zip)
        if self.state_id:
            elements.append(self.state_id.name)
        self.full_location = ', '.join(elements)

    full_location = fields.Char(
        'Full Location', compute='full_location_studio_page'
    )


class ResPartnerEdition(models.Model):
    """Overcharge the definition of a partner to add methods for edit and
    create pages.
    """
    _inherit = 'res.partner'

    @staticmethod
    def get_partner_values():
        """Return the set of data to build edit/create view.

        :return: dict
        """
        return {
            'id': 0,
            'write_date': '',
            'image_url': '',
            'name': '',
            'website': '',
            'email': '',
            'state': '',
            'street': '',
            'street2': '',
            'city': '',
            'zip': '',
            'industry_ids': [],
            'country_id': 0,
            # social network urls
            'social_networks': {
                'twitter': '',
                'youtube': '',
                'vimeo': '',
                'linkedin': '',
                'facebook': '',
            },
            # phone numbers
            'calls': {
                'phone': '',
                'mobile': '',
                'fax': '',
            }

        }

    @api.model
    def build_values_from_kwargs(self, raw_data):
        """Remap the data in kwargs to a mapping that can be processed by
        edition pages.

        For the context, the edition pages when they are process on the server
        can still have error then a write or a create will raise a error. Then
        the data that were supposed to be saved in the partner have to be
        remapped to match what the edition page waits for.

        :param dict raw_data: data from partner.

        :return: remapped data as dict.
        """
        _logger.debug('kwargs: %s', pprint.pformat(raw_data))
        partner_values = self.get_partner_values()
        _logger.debug('partner_values: %s', pprint.pformat(partner_values))

        industry_ids = []

        for key, value in raw_data.iteritems():

            # industries are separated in the raw_data, not part of a single
            # list as expected by the page.
            if 'industry_ids' in key:
                industry_ids.append(int(value))

            elif key in partner_values:

                # country_id is a string but edition page waits it to be a int
                if key in ['country_id']:
                    value = int(value)

                partner_values[key] = value

            elif key in partner_values['calls']:
                partner_values['calls'][key] = value

            elif key in partner_values['social_networks']:
                partner_values['social_networks'][key] = value

        if industry_ids:
            industries = self.env['res.industry']
            partner_values['industry_ids'] = industries.browse(industry_ids)

        _logger.debug('updated partner_values: %s',
                      pprint.pformat(partner_values))

        return partner_values

    @api.model
    def build_values_from_partner(self):
        """Fill up the partner_value from a partner record.

        :return: dict
        """
        websites = self.env['website']
        partner_values = self.get_partner_values()
        partner_values['id'] = self.id
        partner_values['write_date'] = self.write_date
        partner_values['name'] = self.name
        partner_values['image_url'] = websites.image_url(
            self, 'image_medium', size='256x256'
        )
        partner_values['website'] = self.website
        partner_values['email'] = self.email
        partner_values['state'] = self.state
        partner_values['street'] = self.street
        partner_values['street2'] = self.street2
        partner_values['city'] = self.city
        partner_values['zip'] = self.zip
        partner_values['industry_ids'] = self.industry_ids
        partner_values['country_id'] = self.country_id.id
        partner_values['calls']['phone'] = self.phone
        partner_values['calls']['mobile'] = self.mobile
        partner_values['calls']['fax'] = self.fax
        partner_values['social_networks']['linkedin'] = self.linkedin
        partner_values['social_networks']['vimeo'] = self.vimeo
        partner_values['social_networks']['youtube'] = self.youtube
        partner_values['social_networks']['twitter'] = self.twitter
        partner_values['social_networks']['facebook'] = self.facebook

        return partner_values
