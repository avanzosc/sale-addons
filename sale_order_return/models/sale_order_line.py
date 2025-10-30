# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_uom_qty = fields.Float(
        required=False, default=0
    )
    return_qty = fields.Float(
        string="Return Qty",
    )
    
    order_has_pending_returns = fields.Boolean(related="order_id.pending_returns")
    order_has_pending_deliveries = fields.Boolean(related="order_id.pending_deliveries")

    @api.onchange("product_id")
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_uom_qty == 1 and not self.auto_purchase_line_id:
            self.product_uom_qty = 0
        return result
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            return_qty = vals.get("return_qty", 0)
            if return_qty and return_qty > 0:
                order = self.env["sale.order"].browse(vals.get("order_id"))
                if not order or not order.id or order.state in ("draft", "sent"):
                    raise ValidationError(_("Return cannot be created: no delivery has been validated."))
                picking_type = order.type_id.picking_type_id
                return_picking_type = picking_type.return_picking_type_id if picking_type else False
                if order.pending_deliveries:
                    raise ValidationError(_("Cannot create a return: there is a pending delivery picking."))
                if not picking_type or not return_picking_type:
                    raise ValidationError(_("The order has no type or return type configured."))

        return super().create(vals_list)
    
    def write(self, values):
        for line in self:
            if "return_qty" in values:
                new_return_qty = values["return_qty"]
                order = line.order_id
                picking_type = order.type_id.picking_type_id
                return_picking_type = picking_type.return_picking_type_id if picking_type else False
                if order.state not in ("sale", "done") and new_return_qty > 0:
                    raise ValidationError(_("Return cannot be created: no delivery has been validated."))
                if order.pending_deliveries and new_return_qty > 0:
                    raise ValidationError(_("Cannot create a return: there is a pending delivery picking."))
                if (not picking_type or not return_picking_type) and new_return_qty > 0:
                    raise ValidationError(_("The order has no type or return type configured."))
                if new_return_qty < line.return_qty:
                    done_return_moves = line.move_ids.filtered(
                        lambda m: m.state == "done"
                        and m.location_dest_id.usage == "internal"
                        and m.location_id.usage in ("customer", "supplier")
                        and not m.scrapped
                    )
                    if done_return_moves:
                        raise ValidationError(_(
                            "You can't reduce the return quantity because some quantities have already been returned."
                        ))
        res = super(SaleOrderLine, self).write(values)
        if 'return_qty' in values:
            self._create_and_update_return()
        return res
        
    def _create_and_update_return(self):
        if not self:
            return
        sale_order = self.order_id
        picking_type = sale_order.type_id.picking_type_id
        return_picking_type = picking_type.return_picking_type_id

        if sale_order.state != 'sale':
            raise ValidationError(_("Return cannot be created: no delivery has been validated."))
        if sale_order.pending_deliveries:
            raise ValidationError(_("Cannot create a return: there is a pending delivery picking."))
        if not picking_type or not return_picking_type:
            raise ValidationError(_("The order has no type or return type configured."))

        pending_return_picking = sale_order.picking_ids.filtered(
            lambda p: p.picking_type_id == return_picking_type and p.state not in ("done", "cancel")
        )

        if not pending_return_picking:
            pending_return_picking = self.env["stock.picking"].create({
                "partner_id": sale_order.partner_id.id,
                "picking_type_id": return_picking_type.id,
                "location_id": return_picking_type.default_location_src_id.id,
                "location_dest_id": return_picking_type.default_location_dest_id.id,
                "company_id": sale_order.company_id.id,
                "origin": sale_order.name,
                "group_id": sale_order.procurement_group_id.id,
            })
            pending_return_picking.group_id.sale_id = sale_order.id
            
        for line in self.filtered(lambda l: l.order_id == sale_order and l.return_qty > 0):
            done_return_moves = line.move_ids.filtered(
                lambda m: m.state == 'done'
                and m.location_dest_id.usage == 'internal'
                and m.location_id.usage in ('customer', 'supplier')
                and not m.scrapped
            )
            done_qty = sum(done_return_moves.mapped('quantity_done'))
            qty_remaining = line.return_qty - done_qty

            if qty_remaining <= 0:
                continue

            existing_move = pending_return_picking.move_ids_without_package.filtered(
                lambda m: m.sale_line_id == line
            )

            if existing_move:
                existing_move.product_uom_qty = qty_remaining
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
                    "to_refund": True,
                }
                self.env["stock.move"].create(move_vals)
                pending_return_picking.group_id = sale_order.procurement_group_id.id

        pending_return_picking.action_confirm()

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        delivery_lines = self.filtered(lambda l: not l.return_qty or l.return_qty == 0)
        return_lines = self.filtered(lambda l: l.return_qty and l.return_qty > 0)
        result = True
        if delivery_lines:
            if self.order_id.pending_returns:
                raise ValidationError(_("Cannot create a delivery: there is a pending return picking."))
            result = super(SaleOrderLine, delivery_lines)._action_launch_stock_rule(previous_product_uom_qty) 
        for return_line in return_lines:
            if return_line.order_id.state == "sale":
                return_line._create_and_update_return()
        return result
                
