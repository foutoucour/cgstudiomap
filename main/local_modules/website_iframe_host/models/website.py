from openerp import models, fields


class Website(models.Model):
    _inherit = 'website'

    hide_navbar = False


class WebsiteIframeHost(models.Model):
    """Represent the name of a host that can embed our listing."""
    _name = 'website.iframe.host'
    _description = _name

    host = fields.Char('Host', help='Name of the the host that will embed the listing.')
    search_domain = fields.Char(
        'Search Domain',
        help='Domain that will be injected in searches for the given host.'
    )
    hide_navbar = fields.Boolean('Hide Navbar?', default=False)
    light_hosting = fields.Boolean(
        'Light Hosting?', default=False,
        help=(
            'If checked the page like "edit studio" or "add studio" will be redirected'
            'to cgstudiomap.org'
        )
    )
