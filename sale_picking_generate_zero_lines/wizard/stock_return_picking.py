# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    @api.model
    def default_get(self, fields):
        result = super(StockReturnPicking, self).default_get(fields)
        if (
            self.env.context.get("active_id")
            and self.env.context.get("active_model") == "sale.order"
        ):
            sale = self.env["sale.order"].browse(self.env.context.get("active_id"))
            if sale.exists():
                done_pickings = sale.picking_ids.filtered(lambda c: c.state == "done")
                if len(sale.picking_ids) != 1:
                    raise ValidationError(
                        _("You may only return one picking at a time.")
                    )
                elif not done_pickings:
                    raise ValidationError(_("The picking is not done."))
                else:
                    result.update({"picking_id": done_pickings.id})
        return result

    def _create_returns(self):
        new_picking, picking_type_id = super(StockReturnPicking, self)._create_returns()
        return_picking = self.env["stock.picking"].browse(new_picking)
        for return_line in self.product_return_moves:
            if return_line.quantity == 0:
                vals = self._prepare_move_default_values(return_line, return_picking)
                r = return_line.move_id.copy(vals)
                vals = {}
                move_orig_to_link = return_line.move_id.move_dest_ids.mapped(
                    "returned_move_ids"
                )
                move_orig_to_link |= return_line.move_id
                move_orig_to_link |= (
                    return_line.move_id.mapped("move_dest_ids")
                    .filtered(lambda m: m.state not in ("cancel"))
                    .mapped("move_orig_ids")
                    .filtered(lambda m: m.state not in ("cancel"))
                )
                move_dest_to_link = return_line.move_id.move_orig_ids.mapped(
                    "returned_move_ids"
                )
                move_dest_to_link |= (
                    return_line.move_id.move_orig_ids.mapped("returned_move_ids")
                    .mapped("move_orig_ids")
                    .filtered(lambda m: m.state not in ("cancel"))
                    .mapped("move_dest_ids")
                    .filtered(lambda m: m.state not in ("cancel"))
                )
                vals["move_orig_ids"] = [(4, m.id) for m in move_orig_to_link]
                vals["move_dest_ids"] = [(4, m.id) for m in move_dest_to_link]
                vals.update({"to_refund": True})
                r.write(vals)
        return_picking.button_force_done_detailed_operations()
        for line in self.picking_id.move_line_ids_without_package.filtered(
            lambda c: c.qty_done == 0
        ):
            if line.lot_id:
                return_movelines = return_picking.move_line_ids_without_package
                return_line = return_movelines.filtered(
                    lambda c: c.product_id == line.product_id and not (c.lot_id)
                )
                if return_line:
                    return_line[:1].write(
                        {
                            "lot_id": line.lot_id.id,
                        }
                    )
                else:
                    return_line = return_movelines.filtered(
                        lambda c: c.product_id == line.product_id
                    )
                    if return_line:
                        new_return_line = return_line[:1].copy()
                        new_return_line.write(
                            {
                                "lot_id": line.lot_id.id,
                            }
                        )
        return new_picking, picking_type_id
