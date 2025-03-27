# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def button_confirm_pickings(self):
        result = super(SaleOrder, self).button_confirm_pickings()
        for line in self.order_line:
            if (
                line.product_id
                and (line.product_id.tracking != "none")
                and not (line.lot_id)
                and line.return_qty
            ):
                raise ValidationError(
                    _("The product {} has not lot").format(line.product_id.name)
                )
        return result

    def button_return_picking(self):
        has_non_zero_qty = any(line.product_uom_qty != 0 for line in self.order_line)
        has_return_qty = any(line.return_qty != 0 for line in self.order_line)
        if not self.picking_ids and has_non_zero_qty:
            raise ValidationError(_("First you have to do the delivery."))
        elif not self.picking_ids and has_return_qty:
            if not self.type_id:
                raise ValidationError(_("You must enter the order type."))
            elif not self.type_id.picking_type_id:
                raise ValidationError(
                    _("You must enter the picking type of the order type.")
                )
            elif not self.type_id.picking_type_id.return_picking_type_id:
                raise ValidationError(
                    _(
                        "You must enter the return picking type of picking type of the"
                        " order type."
                    )
                )
            self.action_confirm()
            entry_picking = self.picking_ids[0] if self.picking_ids else None
            entry_picking.button_force_done_detailed_operations()
            pick_type = self.type_id.picking_type_id
            picking = self.env["stock.picking"].create(
                {
                    "partner_id": self.partner_id.id,
                    "picking_type_id": pick_type.return_picking_type_id.id,
                    "location_id": entry_picking.location_dest_id.id,
                    "location_dest_id": entry_picking.location_id.id,
                    "company_id": self.company_id.id,
                    "origin": entry_picking.origin,
                }
            )
            picking.group_id.sale_id = self.id
            location_id = picking.location_id.id
            location_dest_id = picking.location_dest_id.id
            move_vals_list = []
            for line in entry_picking.move_line_ids_without_package:
                sale_line = line.move_id.sale_line_id
                return_qty = sale_line.return_qty
                move_vals = {
                    "sale_line_id": sale_line.id,
                    "picking_id": picking.id,
                    "product_id": line.product_id.id,
                    "name": line.move_id.name,
                    "product_uom": line.product_uom_id.id,
                    "product_uom_qty": return_qty,
                    "location_id": location_id,
                    "location_dest_id": location_dest_id,
                    "move_orig_ids": [(4, line.move_id.id)],
                    "origin_returned_move_id": line.move_id.id,
                    "to_refund": True,
                    "move_line_ids": [
                        (
                            0,
                            0,
                            {
                                "picking_id": picking.id,
                                "product_id": line.product_id.id,
                                "product_uom_id": line.product_uom_id.id,
                                "qty_done": return_qty,
                                "location_id": location_id,
                                "location_dest_id": location_dest_id,
                                "lot_id": sale_line.lot_id.id,
                            },
                        )
                    ],
                }
                move_vals_list.append(move_vals)
            moves = self.env["stock.move"].create(move_vals_list)
            for line, move in zip(entry_picking.move_line_ids_without_package, moves):
                line.move_id.write(
                    {
                        "move_dest_ids": [(4, move.id)],
                        "returned_move_ids": [(4, move.id)],
                    }
                )
            picking.group_id = self.procurement_group_id.id
            picking.action_confirm()
            entry_picking.action_cancel()
            entry_picking.sudo().unlink()
            return picking.button_validate()
        picking_act = super(SaleOrder, self).button_return_picking()
        picking = self.env["stock.picking"].browse(picking_act.get("res_id"))
        if len(picking) == 1:
            for line in picking.move_line_ids_without_package:
                if line.move_id.sale_line_id:
                    line.qty_done = line.move_id.sale_line_id.return_qty
            return (
                picking_act
                if not any(line.return_qty != 0 for line in self.order_line)
                else picking.button_validate()
            )
