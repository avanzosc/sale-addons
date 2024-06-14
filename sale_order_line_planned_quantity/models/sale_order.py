# Copyright (c) 2024 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    difference_between_ordered_planned = fields.Boolean(
        string="Difference Between Ordered And Planned", store=True, copy=False,
        compute="_compute_planned_quantity",)

    @api.depends("order_line", "order_line.product_uom_qty", "order_line.state",
                 "order_line.move_ids", "order_line.move_ids.state",
                 "order_line.move_ids.product_uom_qty",
                 "order_line.move_ids.picking_type_id",
                 "order_line.move_ids.picking_type_id.use_to_calculate_planned_quantities")
    def _compute_planned_quantity(self):
        for sale in self:
            difference_between_ordered_planned = False
            for line in sale.order_line:
                planned_quantity = 0
                if line.move_ids:
                    moves = line.move_ids.filtered(
                        lambda x: x.state != "cancel" and x.picking_type_id and
                        x.picking_type_id.use_to_calculate_planned_quantities)
                    if moves:
                        planned_quantity = sum(moves.mapped("product_uom_qty"))
                if (line.product_uom_qty != planned_quantity and
                        line.state != "draft"):
                    difference_between_ordered_planned = True
            sale.difference_between_ordered_planned = (
                difference_between_ordered_planned)
