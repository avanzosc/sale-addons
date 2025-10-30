# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(required=False)
    return_qty = fields.Float(string="Return Qty")

    @api.onchange("product_id")
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_uom_qty == 1 and not self.auto_purchase_line_id:
            self.product_uom_qty = 0
        return result

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        for line in lines:
            if line.return_qty and line.return_qty > 0:
                line._create_and_update_return()
        return lines

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
        res = super(SaleOrderLine, self).write(values)
        if "return_qty" in values:
            self._create_and_update_return()
        return res

    def _create_and_update_return(self):
        sale_order = self.order_id

        # Validate that picking types are configured
        picking_type = sale_order.type_id.picking_type_id
        return_picking_type = picking_type.return_picking_type_id
        if not picking_type or not return_picking_type:
            raise ValidationError(_("The order has no type or return type configured."))

        # Find existing pending return picking
        pending_return_picking = sale_order.picking_ids.filtered(
            lambda p: p.picking_type_id == return_picking_type
            and p.state not in ("done", "cancel")
        )

        # No pending return found
        if not pending_return_picking:
            # Create return picking
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

        # Pending return found
        for line in self.filtered(
            lambda l: l.order_id == sale_order and l.return_qty > 0
        ):
            # Calculate already returned quantities
            done_return_moves = line.move_ids.filtered(
                lambda m: m.state == "done"
                and m.location_dest_id.usage == "internal"
                and m.location_id.usage in ("customer", "supplier")
                and not m.scrapped
            )
            done_qty = sum(done_return_moves.mapped("quantity_done"))

            # Calculate remaining quantity to return
            qty_remaining = line.return_qty - done_qty

            # Skip if no quantity remaining to return
            if qty_remaining <= 0:
                continue

            existing_move = pending_return_picking.move_ids_without_package.filtered(
                lambda m: m.sale_line_id == line
            )

            # Existing move found: update with new remaining quantity
            if existing_move:
                existing_move.product_uom_qty = qty_remaining
                if line.lot_id and existing_move.state == "draft":
                    existing_move.restrict_lot_id = line.lot_id.id

            # No existing move found: create new move
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

        # Ensure the picking is linked to the sale order
        if pending_return_picking and not pending_return_picking.sale_id:
            pending_return_picking.sale_id = sale_order.id
        # Confirm the picking
        pending_return_picking.action_confirm()

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        delivery_lines = self.filtered(lambda l: not l.return_qty or l.return_qty == 0)
        return_lines = self.filtered(lambda l: l.return_qty and l.return_qty > 0)
        result = True
        # Process delivery lines using standard stock rules
        if delivery_lines:
            result = super(SaleOrderLine, delivery_lines)._action_launch_stock_rule(
                previous_product_uom_qty
            )

        # Process return lines by creating return pickings
        for return_line in return_lines:
            return_line._create_and_update_return()
        return result

    @api.depends(
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
        "return_qty",
        "move_ids.quantity_done",
    )
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()
        for line in self:
            if line.return_qty and line.return_qty > 0:
                line.product_uom_qty = line.qty_delivered
