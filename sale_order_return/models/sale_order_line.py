# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(required=False)
    return_qty = fields.Float()

    @api.onchange("product_id")
    def _onchange_product_id_reset_qty(self):
        if self.product_uom_qty == 1 and not self.auto_purchase_line_id:
            self.product_uom_qty = 0

    def write(self, values):
        for line in self:
            if "return_qty" in values:
                new_return_qty = values["return_qty"]
                if new_return_qty < line.return_qty:
                    done_return_moves = line.move_ids.filtered(
                        lambda m: m.state == "done"
                        and m.location_dest_id.usage == "internal"
                        and m.location_id.usage in ("customer", "supplier")
                        and not m.scrapped
                    )
                    if done_return_moves:
                        raise ValidationError(
                            _("Some qtys were already returned, qty can't be reduced.")
                        )
        res = super().write(values)
        if "return_qty" in values:
            confirmed = self.filtered(lambda line: line.order_id.state == "sale")
            if confirmed:
                confirmed._create_and_update_return()
        return res

    def _create_and_update_return(self):
        sale_order = self.order_id

        picking_type = sale_order.type_id.picking_type_id
        if not picking_type:
            raise ValidationError(_("The order has no operation type configured."))
        return_picking_type = picking_type.return_picking_type_id
        if not return_picking_type:
            raise ValidationError(
                _("The order has no return operation type configured.")
            )

        pending_return_picking = sale_order.picking_ids.filtered(
            lambda p: p.picking_type_id == return_picking_type
            and p.state not in ("done", "cancel")
        )

        lines_with_remaining = []
        for line in self.filtered(
            lambda line: line.order_id == sale_order and line.return_qty > 0
        ):
            done_return_moves = line.move_ids.filtered(
                lambda m: m.state == "done"
                and m.location_dest_id.usage == "internal"
                and m.location_id.usage in ("customer", "supplier")
                and not m.scrapped
            )
            done_qty = sum(done_return_moves.mapped("quantity"))
            qty_remaining = line.return_qty - done_qty
            if qty_remaining > 0:
                lines_with_remaining.append((line, qty_remaining))

        if not lines_with_remaining:
            return

        if not pending_return_picking:
            pending_return_picking = self.env["stock.picking"].create(
                {
                    "partner_id": sale_order.partner_id.id,
                    "picking_type_id": return_picking_type.id,
                    "location_id": sale_order.partner_id.property_stock_customer.id,
                    "location_dest_id": return_picking_type.default_location_dest_id.id,
                    "company_id": sale_order.company_id.id,
                    "origin": sale_order.name,
                    "group_id": sale_order.procurement_group_id.id,
                    "sale_id": sale_order.id,
                }
            )

        for line, qty_remaining in lines_with_remaining:
            existing_move = pending_return_picking.move_ids_without_package.filtered(
                lambda m, line=line: m.sale_line_id == line
            )
            if existing_move:
                existing_move.product_uom_qty = qty_remaining
                if line.lot_id and existing_move.state == "draft":
                    existing_move.restrict_lot_id = line.lot_id.id
            else:
                move_vals = {
                    "sale_line_id": line.id,
                    "picking_id": pending_return_picking.id,
                    "product_id": line.product_id.id,
                    "name": line.name or line.product_id.display_name,
                    "product_uom": line.product_uom.id,
                    "product_uom_qty": qty_remaining,
                    "location_id": pending_return_picking.location_id.id,
                    "location_dest_id": pending_return_picking.location_dest_id.id,
                    "company_id": sale_order.company_id.id,
                    "group_id": sale_order.procurement_group_id.id,
                    "restrict_lot_id": line.lot_id.id if line.lot_id else False,
                    "to_refund": True,
                }
                self.env["stock.move"].create(move_vals)
                pending_return_picking.group_id = sale_order.procurement_group_id.id

        if not pending_return_picking.sale_id:
            pending_return_picking.sale_id = sale_order.id
        pending_return_picking.action_confirm()

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id)
        if not values.get("warehouse_id") and self.order_id.warehouse_id:
            values["warehouse_id"] = self.order_id.warehouse_id
        return values

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        delivery_lines = self.filtered(
            lambda line: not line.return_qty or line.return_qty == 0
        )
        return_lines = self.filtered(
            lambda line: line.return_qty and line.return_qty > 0
        )
        result = True
        if delivery_lines:
            result = super(SaleOrderLine, delivery_lines)._action_launch_stock_rule(
                previous_product_uom_qty=previous_product_uom_qty
            )
        for return_line in return_lines:
            return_line._create_and_update_return()
        return result

    @api.depends(
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
        "return_qty",
        "move_ids.quantity",
    )
    def _compute_qty_delivered(self):
        res = super()._compute_qty_delivered()
        for line in self:
            if line.return_qty and line.return_qty > 0:
                line.product_uom_qty = line.qty_delivered
        return res
