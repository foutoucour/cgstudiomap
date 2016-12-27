# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
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
from pprint import pformat

from openerp import models, api
from openerp.exceptions import except_orm
from openerp.tools.translate import _
from pygeocoder import Geocoder, GeocoderError

_logger = logging.getLogger(__name__)
__codec__ = 'utf-8'


class ResPartner(models.Model):
    """Add Social Networks fields."""
    _inherit = 'res.partner'
    # set on to avoid that some function are called during tests.
    __dryRun__ = False

    @api.model
    def _build_geocode(self, vals=None):
        """Build the geocode from the data from the user.

        The Geocode is built from the street, city, zip, state and country
        details from the record.

        The Geocode is built from the the data in vals completed by the data
        in the record itself.
        If self.__dryRun__ is set to True, the build is skipped.

        :param vals: set of values for the record. Default: {}
        :return: Geocoder.geocode instance
        """
        if self.__dryRun__:
            return None

        def get_data(field_name):
            data = vals.get(field_name)
            field = getattr(self, field_name)
            if not data and field:
                data = field
            if not data:
                return ''
            data = data.encode(__codec__)
            _logger.debug('data ({}): {}'.format(field_name, data))

            return data

        _logger.debug('_build_geocode')
        if vals is None:
            vals = {}
        _logger.debug('vals: {}'.format(vals))

        location = get_data('street')
        # Don't get street2 into the geocode it might screw the location
        # actually.
        city = get_data('city')
        zip_ = get_data('zip')

        location = ' '.join([location, city, zip_])
        _logger.debug(
            'location (street, street2, city, zip): {}'.format(location)
        )
        state_id = vals.get('state_id')
        _logger.debug('vals.get(state_id): {}'.format(state_id))
        if state_id:
            location = ' '.join([
                location,
                self.env['res.country.state'].browse(state_id).name.encode(
                    __codec__)
            ])

        elif self.state_id:
            state_name = self.state_id.name.encode(__codec__)
            _logger.debug(
                'self.state_id.name: {}'.format(state_name)
            )

            location = ' '.join([location, state_name])
        _logger.debug('location (state): {}'.format(location))

        country_id = vals.get('country_id')
        _logger.debug('vals.get("country_id"): {}'.format(country_id))
        if country_id:
            location = ' '.join([
                location,
                self.env['res.country'].browse(country_id).name.encode(
                    __codec__)
            ])
        elif self.country_id:
            country_name = self.country_id.name.encode(__codec__)
            _logger.debug('country_name: {}'.format(country_name))
            location = ' '.join([location, country_name])
        _logger.debug('location (country): {}'.format(location))

        location = location.strip()
        _logger.debug('bool(location): {}'.format(bool(location)))

        if location:
            # https://github.com/cgstudiomap/cgstudiomap/issues/64
            # If the address is not localized, Geocoder raises a GeocoderError
            # The raise results to a traceback that can be scary for the user
            # It is so necessary to put this traceback in a more user-friendly
            # report
            try:
                geocode = Geocoder.geocode(location)
            except GeocoderError as e:
                raise except_orm(
                    _('Error'),
                    _('The address cannot be geolocalized. '
                      'Please enter a valid address.'
                      '\n\nError details: {}'.format(e)
                      )
                )
            _logger.debug('geocode: {}'.format(geocode))

            if geocode.route is None:
                return None

            return geocode

        _logger.debug('Empty Location, returning None')
        return None

    @api.model
    def _clean_location_data(self, vals):
        """Build a geocode from the details of the partner to then inject
        into the records the cleaned data caught from google.

        If self.__dryRun__ is set to True, the clean is skipped.

        :return: dict with the values for the orm.
        """
        if self.__dryRun__:
            return vals

        _logger.debug('_clean_location_data')
        _logger.debug('vals: {}'.format(vals))
        # https://github.com/cgstudiomap/cgstudiomap/issues/71
        # The validation of the address has to be triggered if
        # any of the field related to the address is changed.
        # That is translated by the prescence of the field in the
        # keys of vals.
        # Street2 is excluded here as it is not really involved in the
        # geolocation.
        address_related_fields = {'street', 'city', 'country_id', 'zip'}

        # Test if none of the fields are present in vals.
        # set & set is the intersection of both sets.
        if not address_related_fields & set(vals):
            _logger.debug(
                'No field related to address was found. '
                'Skipping Location data cleaning'
            )
            return vals

        # First a geocode is build from the data of the record.
        # the build is done with the data from vals completed by
        # the data in the record (in case of write ie)
        geocode = self._build_geocode(vals)

        if geocode is None:
            _logger.debug('The location values might not be in the vals.')
            return vals

        if geocode.route is None:
            _logger.debug('The route values might not be in the vals.')
            return vals

        # then the cleaned data are reinjected to the values the
        # record will be created/written with.
        street_number = geocode.street_number
        _logger.debug('Checking if there is a street number.')
        if street_number is not None:
            vals['street'] = ' '.join(
                [geocode.street_number, geocode.route]
            )
        else:
            vals['street'] = geocode.route.encode(__codec__)

        _logger.debug('val["street"]: %s', vals['street'])
        # https://github.com/cgstudiomap/cgstudiomap/issues/145
        # avoid zip code to be nonetype.
        zip_code = geocode.postal_code or vals['zip'] or self.zip or 0
        vals['zip'] = zip_code.encode(__codec__)
        _logger.debug('val["zip"]: %s', vals['zip'])
        # https://github.com/cgstudiomap/cgstudiomap/issues/139
        # it seems sometimes geocode can't define a city value
        # we then takes the sublocality value to avoid to have a None value.
        city = (
            geocode.city
            or geocode.postal_town
            or geocode.sublocality
            or geocode.administrative_area_level_1
        )
        vals['city'] = city.encode(__codec__)
        _logger.debug('val["city"]: %s', vals['city'])

        # Getting the country of the location
        # Normally all the countries are registered to odoo by default.
        country_pool = self.env['res.country']
        country = country_pool.search(
            [('code', '=', geocode.country__short_name)]
        )

        if country:
            vals['country_id'] = country.id
            _logger.debug('val["country_id"]: %s', vals['country_id'])

        # the case of state is a bit more tricky.
        # all the countries don't have state.
        _logger.debug('Checking states.')
        if geocode.state:
            # Even tho, all the states are not registered by default to odoo.
            # We have first to check if there is a record for the given state
            # code (state__short__name)
            state_pool = self.env['res.country.state']
            state = state_pool.search(
                [
                    ('code', '=', geocode.state__short_name),
                    ('country_id', '=', country.id)
                ],
                limit=1
            )
            _logger.debug('state: %s', state)
            # Checking the search returned something
            # otherwise that means it needs to be created.
            if not state:
                state = state_pool.create({
                    'country_id': country.id,
                    'name': geocode.state__long_name,
                    'code': geocode.state__short_name,
                })

            vals['state_id'] = state.id
            _logger.debug('val["state_id"]: %s', vals['state_id'])

        _logger.debug('vals: {}'.format(vals))
        return vals

    @api.model
    def create(self, vals):
        _logger.debug('res_partner_location_validation.create')
        vals = self._clean_location_data(vals)
        _logger.debug('_clean_location_data: {}'.format(pformat(vals)))
        ret = super(ResPartner, self).create(vals)
        _logger.debug('ret: {}'.format(ret))
        return ret

    @api.multi
    def write(self, vals):
        return super(ResPartner, self).write(self._clean_location_data(vals))
