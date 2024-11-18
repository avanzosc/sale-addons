# Copyright (c) 2024 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    planned_quantity = fields.Float(
        string="Planned Quantity",
        compute="_compute_planned_quantity",
        digits="Product Unit of Measure",
        compute_sudo=True,
        store=True,
        copy=False,
    )
    difference_between_ordered_planned = fields.Boolean(
        string="Difference Between Ordered And Planned",
        compute_sudo=True,
        store=True,
        copy=False,
        compute="_compute_planned_quantity",
    )

    @api.depends(
        "product_uom_qty",
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
    )
    def _compute_planned_quantity(self):
        for line in self:
            # TODO: maybe one day, this should be done in SQL for performance sake
            if line.qty_delivered_method == "stock_move":
                planned_qty = 0.0
                outgoing_moves, incoming_moves = line._get_outgoing_incoming_moves()
                for move in outgoing_moves:
                    if move.state == "cancel":
                        continue
                    planned_qty += move.product_uom._compute_quantity(
                        move.product_uom_qty,
                        line.product_uom,
                        rounding_method="HALF-UP",
                    )
                for move in incoming_moves:
                    if move.state == "cancel":
                        continue
                    planned_qty -= move.product_uom._compute_quantity(
                        move.product_uom_qty,
                        line.product_uom,
                        rounding_method="HALF-UP",
                    )
            else:
                planned_qty = line.product_uom_qty
            line.update(
                {
                    "planned_quantity": planned_qty,
                    "difference_between_ordered_planned": bool(
                        line.product_uom_qty != planned_qty
                    ),
                }
            )
