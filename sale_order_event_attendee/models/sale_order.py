# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("order_line")
    def _calculate_order_line_qty(self):
        for line in self.order_line:
            if line.product_id.event_ok:
                line_count = self.env["event.registration"].search_count(
                    [
                        ("sale_order_id", "=", self.id),
                        ("sale_order_line_id", "=", line._origin.id),
                    ]
                )
                if line_count > 0:
                    line.product_uom_qty = line_count
