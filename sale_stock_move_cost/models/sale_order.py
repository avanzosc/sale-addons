# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_order_cost = fields.Float(
        string="Total Cost",
        digits="Product Price",
        copy=False,
        store=True,
        compute="_compute_sale_order_cost_margin",
    )
    sale_order_margin = fields.Float(
        string="Total Margin",
        digits="Product Price",
        copy=False,
        store=True,
        compute="_compute_sale_order_cost_margin",
    )

    @api.depends(
        "order_line",
        "order_line.move_ids",
        "order_line.move_ids.move_line_ids",
        "order_line.move_ids.move_line_ids.cost",
    )
    def _compute_sale_order_cost_margin(self):
        for sale in self:
            sale_order_cost = 0
            sale_order_margin = 0
            for line in sale.order_line:
                sale_line_cost = 0
                moves = line.move_ids.filtered(lambda x: x.state != "cancel")
                for move in moves:
                    sale_line_cost += sum(move.move_line_ids.mapped("cost"))
                    sale_order_cost += sale_line_cost
                if sale_line_cost > 0:
                    sale_order_margin += line.price_subtotal - sale_line_cost
            sale.sale_order_cost = sale_order_cost
            sale.sale_order_margin = sale_order_margin
