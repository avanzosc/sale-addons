# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    order_status = fields.Selection(
        string='Order status', comodel_name='sale.order',
        related='sale_order_id.state')
