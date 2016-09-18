import logging
import datetime
from openerp import models, api

log = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Addition of method to create rel_type_viewed relations."""
    _inherit = 'res.partner'

    @api.model
    def add_viewed_by_relation(self, partner):
        """Create a relation rel_type_viewed with assuming self is the company."""
        viewed_relation_type = self.env['ir.model.data'].get_object(
            'res_partner_relations_viewed', 'rel_type_viewed'
        )
        relation_pool = self.env['res.partner.relation']
        today = datetime.date.today()
        relation_pool.create(
            {
                'left_partner_id': self.id,
                'right_partner_id': partner.id,
                'type_id': viewed_relation_type.id,
                'date_start': today,
                'date_end': today,
            }
        )
