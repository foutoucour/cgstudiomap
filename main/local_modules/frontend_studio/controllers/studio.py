# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)
from openerp.addons.frontend_listing.controllers.listing import Listing

from openerp import http
from openerp.exceptions import ValidationError, except_orm
from openerp.http import request

logger = logging.getLogger(__name__)

partner_url = '/directory/company'


class Studio(Base):
    """Representation of the homepage of the website."""

    @statsd.timed(
        'odoo.frontend.studio.view.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>'.format(partner_url),
        type='http', auth="public", website=True
    )
    def view(self, partner, **dummy):
        """Render the page of a studio in view mode.

        During the process a relation viewed/viewed by is created.
        :param object partner: record of a res.partner.
        :param dummy: implemented to dodge the 500 error described in
            https://github.com/cgstudiomap/cgstudiomap/issues/631
            It is actually not used later in the function.

        :return: request.render
        """
        del dummy  # not used.
        values = self.common_values()
        values['partner'] = partner
        partner_values = partner.get_partner_values()
        values['social_networks'] = partner_values['social_networks'].keys()

        marquee_plus_social_network = any(
            not getattr(partner, field) for field in values['social_networks']
        )
        logger.debug(
            'marqueePlusSocialNetwork: %s', marquee_plus_social_network
        )
        values.update({
            'marqueePlusSocialNetwork': marquee_plus_social_network,
            'partners': partner.get_random_studios_from_same_location(6),
            'filter_domain': partner.country_id.name,
        })
        user_partner = request.env['res.users'].browse(request.uid).partner_id
        partner.add_viewed_by_relation(user_partner)
        return request.website.render('frontend_studio.view', values)

    @statsd.timed(
        'odoo.frontend.studio.edit.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>/edit'.format(partner_url),
        type='http', methods=['GET'], auth="user", website=True
    )
    def edit(self, partner):
        """Render the page of a studio in edit mode

        :param object partner: record of a res.partner.
        :return: request.render
        """
        return request.website.render(
            'frontend_studio.edit', self.get_values_for_edition_page(
                partner=partner
            )
        )

    @statsd.timed(
        'odoo.frontend.studio.create.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/create'.format(partner_url),
        type='http', methods=['GET'], auth="user", website=True
    )
    def create(self):
        """Render the page to create a new res partner in the database."""
        values = self.get_values_for_edition_page()
        values['create'] = True
        return request.website.render('frontend_studio.edit', values)

    def get_values_for_edition_page(self, partner=None, kwargs=None):
        """Gather the details needed to render page that edit or create a
        partner. If a partner is given, the value are built from it.

        :param object partner: record of a res.partner. Default: None.
        :param dict kwargs: mapping of values to work with.
            kwargs most likely come from an edition page (edit or create).
            The aim here is to remap the values in kwargs to be processed
            in the edition page.

        :return: mapping of the value to render the page with.
        :rtype: dict
        """
        values = self.common_values()
        partner_pool = request.env['res.partner']
        if partner:
            # map the values of a res.partner record to a structure that
            # an edition page will process.
            partner_values = partner.build_values_from_partner()
        elif kwargs:
            # remap the values in kwargs to a structure that can be processed
            # by an edition page.
            partner_values = partner_pool.build_values_from_kwargs(kwargs)
        else:
            # get the empty dict that will allow to render an edition page
            # with all fields as empty.
            partner_values = partner_pool.get_partner_values()

        values['partner'] = partner_values

        values.update({
            'countries': request.env['res.country'].search([]),
            'industries': request.env['res.industry'].search([]),
            'partner_pool': request.env['res.partner'],
            'getattr': getattr,
        })
        return values

    @staticmethod
    def common_values():
        """Build the values shared by different views of the module.

        :return: mapping for values for all the views.
        """
        logger.debug('common_values')
        keep = QueryURL()

        partner = request.env['res.partner'].browse(1)
        fields = partner.fields_get()
        state_selections = fields['state']['selection']
        logger.debug('selections: %s', state_selections)

        return {
            'fields': fields,
            'partner': partner,
            'keep': keep,
            'state_selections': state_selections,
            'getattr': getattr,
        }


class StudioPost(Studio):
    """Control of POST methods for the studio page."""
    @statsd.timed(
        'odoo.frontend.studio.save.time',
        tags=['frontend', 'frontend:studio', 'POST']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>/edit'.format(partner_url),
        type='http', auth="public", methods=['POST'], website=True
    )
    def save(self, partner, **kwargs):
        """Save new data of the partner then return the request to render
        the page following the edition.

        :param object partner: record of a res.partner.
        :param dict kwargs: list of fields to update.
        :return: request.render
        """
        logger.debug('save')
        logger.debug('kwargs: %s', kwargs)

        try:
            partner.write_from_post_request(kwargs)
        except ValidationError as err:

            # if a validation error has been raised,
            # we go back to the edit page, so the user can fix the error.
            values = self.get_values_for_edition_page(partner=partner)
            # website is part of the kwargs, but it interfers with a call of
            # website module.
            del kwargs['website']
            values.update(kwargs)
            values['error'] = err[-1]
            return request.website.render('frontend_studio.edit', values)

        values = {
            'partner': partner,
            'partner_url': '/'.join([partner_url, str(partner.id)]),
            'map_url': Listing.map_url,
        }
        return request.website.render('frontend_studio.thank_you', values)


    @statsd.timed(
        'odoo.frontend.studio.save_new.time',
        tags=['frontend', 'frontend:studio', 'POST']
    )
    @http.route(
        '{0}/create'.format(partner_url),
        type='http', auth="public", methods=['POST'], website=True
    )
    def save_new(self, **kwargs):
        """Try to save a new partner from the given data.

        :param dict kwargs: list of fields to update.
        :return: request.render
        """
        logger.debug('save_new')
        logger.debug('kwargs: %s', kwargs)
        partner_pool = request.env['res.partner']
        try:
            partner = partner_pool.create_from_post_request(kwargs)
        except (ValidationError, except_orm) as err:

            values = self.get_values_for_edition_page(kwargs=kwargs)
            del kwargs['website']
            values.update(kwargs)
            values['error'] = err[-1]
            values['create'] = True
            return request.website.render('frontend_studio.edit', values)

        values = {
            'partner': partner,
            'partner_url': '/'.join([partner_url, str(partner.id)]),
            'map_url': Listing.map_url,
        }
        return request.website.render('frontend_studio.thank_you', values)
