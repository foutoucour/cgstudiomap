# -*- coding: utf-8 -*-
from collections import defaultdict

import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class MainPage(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        _logger.debug('index')
        page = 'homepage'
        cr, uid, context = request.cr, request.uid, request.context
        pool = request.registry
        partner_pool = pool['res.partner']
        country_pool = pool['res.country']
        ir_model_data_pool = pool['ir.model.data']
        media = ir_model_data_pool.get_object(
            cr, uid, 'res_partner_industry', 'med'
        )
        ammap_homepage = ir_model_data_pool.get_object(
            cr, uid, 'frontend', 'homepage_ammap_config', context=context
        )

        by_countries = defaultdict(int)
        for country in country_pool.search(cr, uid, [], context=context):
            number_partners = len(
                partner_pool.search(
                    cr, uid,
                    [
                        ('active', '=', True),
                        ('is_company', '=', True),
                        ('industry_family_ids', 'in', [media.id]),
                        ('country_id', '=', country)
                    ],
                    context=context
                )
            )
            if number_partners:
                by_countries[
                    country_pool.browse(cr, uid, country, context=context)
                ] = number_partners

        values = {
            'page': page,
            'geochart_data': by_countries,
            'geochart_target': 'geochart_div',
            'ammap_config': ammap_homepage,
        }

        return request.render('frontend.homepage', values)
