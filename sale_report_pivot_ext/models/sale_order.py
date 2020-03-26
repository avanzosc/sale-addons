# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from pytz import timezone, utc

str2datetime = fields.Datetime.from_string


def _convert_to_local_date(date, tz=u'UTC'):
    if not date:
        return False
    if not tz:
        tz = u'UTC'
    new_date = str2datetime(date) if isinstance(date, str) else date
    new_date = new_date.replace(tzinfo=utc)
    local_date = new_date.astimezone(timezone(tz)).replace(tzinfo=None)
    return local_date


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commitment_date_without_hour = fields.Date(
        string='Commitment date without hour', store=True,
        compute='_compute_commitment_date_without_hour')

    @api.depends('commitment_date')
    def _compute_commitment_date_without_hour(self):
        tz = self.env.user.tz
        for line in self.filtered('commitment_date'):
            line.commitment_date =\
                _convert_to_local_date(line.commitment_date, tz=tz)
