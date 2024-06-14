# Copyright (c) 2024 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    planned_quantity = fields.Float(
        string="Planned Quantity", compute="_compute_planned_quantity",
        digits="Product Unit of Measure", store=True, copy=False
    )
    difference_between_ordered_planned = fields.Boolean(
        string="Difference Between Ordered And Planned", store=True, copy=False,
        compute="_compute_planned_quantity",)

    @api.depends("product_uom_qty", "state", "move_ids", "move_ids.state",
                 "move_ids.product_uom_qty", "move_ids.picking_type_id",
                 "move_ids.picking_type_id.use_to_calculate_planned_quantities")
    def _compute_planned_quantity(self):
        for line in self:
            planned_quantity = 0
            difference_between_ordered_planned = False
            if line.move_ids:
                moves = line.move_ids.filtered(
                    lambda x: x.state != "cancel" and x.picking_type_id and
                    x.picking_type_id.use_to_calculate_planned_quantities)
                if moves:
                    planned_quantity = sum(moves.mapped("product_uom_qty"))
            if (line.product_uom_qty != planned_quantity and
                    line.state != "draft"):
                difference_between_ordered_planned = True
            line.planned_quantity = planned_quantity
            line.difference_between_ordered_planned = (
                difference_between_ordered_planned)
