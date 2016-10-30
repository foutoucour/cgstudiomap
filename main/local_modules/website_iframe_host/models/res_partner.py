import logging
from openerp import models
from openerp.http import request

logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def link_to_studio_page(self, *args, **kwargs):
        """Overcharge the method to add a _target=blank.
        """
        link = super(ResPartner, self).link_to_studio_page(*args, **kwargs)
        # test if a request has been done.
        try:
            host_name = request.httprequest.host
        except AttributeError:
            logger.exception('request not defined.')
            return link

        # if so let's see the config of the host.
        website_iframe_host_pool = self.env['website.iframe.host']
        iframe_host = website_iframe_host_pool.search(
            [('host', '=', host_name)], limit=1
        )
        if iframe_host and iframe_host.light_hosting:
            link = link.replace('<a', '<a target="_blank"')

        return link
