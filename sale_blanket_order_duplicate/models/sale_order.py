# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    blanket_order_id = fields.Many2one(store=True, copy=True)

    @api.depends(
        "order_line",
        "order_line.blanket_order_line",
        "order_line.blanket_order_line.order_id",
    )
    def _compute_blanket_order_id(self):
        return super()._compute_blanket_order_id()
