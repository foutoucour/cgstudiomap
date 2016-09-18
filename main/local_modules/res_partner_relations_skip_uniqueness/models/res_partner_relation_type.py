import logging
from openerp import models, api, fields

log = logging.getLogger(__name__)


class ResPartnerRelationType(models.Model):
    """Addition of the field skip_uniqueness"""
    _inherit = 'res.partner.relation.type'

    skip_uniqueness = fields.Boolean(
        "Skip Uniqueness",
        default=False,
        help='Skip the check of uniquess and allow duplicata.'
    )


class ResPartnerRelation(models.Model):
    """Addition of the new behaviour according to skip_uniqueness."""
    _inherit = 'res.partner.relation'

    @api.one
    @api.constrains('left_partner_id', 'right_partner_id', 'active')
    def _check_relation_uniqueness(self):
        """Overcharge the check to be skipped if the record allows duplication."""
        if self.type_id.skip_uniqueness:
            log.debug('Uniqueness skipped!')
            return
        return super(ResPartnerRelation, self)._check_relation_uniqueness()
