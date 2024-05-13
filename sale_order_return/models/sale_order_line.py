# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(
        required=False,
    )
    return_qty = fields.Float(
        string="Return Qty",
    )

    @api.onchange("product_id")
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_uom_qty == 1 and not self.auto_purchase_line_id:
            self.product_uom_qty = 0
        return result

    @api.model
    def create(self, values):
        line = super().create(values)
        if "return_qty" in values:
            done_picking = line.order_id.picking_ids.filtered(
                lambda c: c.state == "done")
            if done_picking:
                for move in line.move_ids:
                    if move.picking_id != done_picking[:1]:
                        picking = move.picking_id
                        move.picking_id = done_picking[:1].id
                        move.state = "done"
                        if not move.move_line_ids:
                            self.env["stock.move.line"].create(
                                move._prepare_move_line_vals()
                            )
                        if not picking.move_ids_without_package:
                            picking.unlink()
        return line
