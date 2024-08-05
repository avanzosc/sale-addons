# Copyright (c) 2024 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    planned_quantity = fields.Float(
        string="Planned Quantity",
        compute="_compute_planned_quantity",
        digits="Product Unit of Measure",
        store=True,
        copy=False,
    )
    difference_between_ordered_planned = fields.Boolean(
        string="Difference Between Ordered And Planned",
        store=True,
        copy=False,
        compute="_compute_difference_between_ordered_planned",
    )

    @api.depends(
        "product_uom_qty",
        "state",
        "move_ids",
        "move_ids.state",
        "move_ids.product_uom_qty",
        "move_ids.picking_type_id",
        "move_ids.picking_type_id.use_to_calculate_planned_quantities",
    )
    def _compute_planned_quantity(self):
        for line in self:
            planned_quantity = 0
            moves_planned_quantities = False
            if line.move_ids:
                moves_planned_quantities = line.move_ids.filtered(
                    lambda x: x.picking_type_id.use_to_calculate_planned_quantities
                )
                if moves_planned_quantities:
                    moves = moves_planned_quantities.filtered(
                        lambda x: x.state != "cancel"
                    )
                    if moves:
                        planned_quantity = sum(moves.mapped("product_uom_qty"))
            line.planned_quantity = planned_quantity if moves_planned_quantities else 0

    @api.depends(
        "planned_quantity",
        "state",
        "product_uom_qty",
    )
    def _compute_difference_between_ordered_planned(self):
        for line in self:
            moves_planned_quantities = False
            if line.move_ids:
                moves_planned_quantities = line.move_ids.filtered(
                    lambda x: x.picking_type_id.use_to_calculate_planned_quantities
                )
            if moves_planned_quantities:
                line.difference_between_ordered_planned = bool(
                    line.product_uom_qty != line.planned_quantity
                    and line.state != "draft"
                )
            else:
                line.difference_between_ordered_planned = False
