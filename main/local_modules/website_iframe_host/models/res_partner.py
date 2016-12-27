import logging
import re

from openerp import models

from openerp.addons.website_iframe_host.controllers.base import (
    is_website_light_hosting
)

logger = logging.getLogger(__name__)


def add_target_blank_to_a(html):
    """find all links to company page in the given html code and add _target to it."""
    pattern = '<a '
    replacement = '<a target="_blank" '
    return re.sub(pattern, replacement, html)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def link_to_studio_page(self, *args, **kwargs):
        """Overcharge the link to studio if the iframe is light hosting."""
        ret = super(ResPartner, self).link_to_studio_page(*args, **kwargs)
        if is_website_light_hosting():
            ret = add_target_blank_to_a(ret)
        return ret
