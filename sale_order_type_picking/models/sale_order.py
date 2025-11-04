# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    carrier_id = fields.Many2one(
        compute="_compute_carrier_id", store=True, readonly=False
    )

    @api.depends("type_id")
    def _compute_carrier_id(self):
        res = None
        if hasattr(super(), "_compute_carrier_id"):
            res = super()._compute_carrier_id()
        for order in self.filtered("type_id"):
            order_type = order.type_id
            if order_type.carrier_id:
                order.carrier_id = order_type.carrier_id.id
        return res
