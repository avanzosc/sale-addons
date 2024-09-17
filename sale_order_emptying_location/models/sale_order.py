# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_empty_location = fields.Boolean(
        string="Show Emptying Location",
        compute="_compute_show_empty_location",
    )

    @api.depends(
        "type_id",
        "type_id.picking_type_id",
        "type_id.picking_type_id.default_location_src_id",
        "state",
    )
    def _compute_show_empty_location(self):
        for sale in self:
            show_empty_location = False
            if (
                sale.type_id
                and sale.type_id.picking_type_id
                and sale.type_id.picking_type_id.default_location_src_id
                and sale.state == "draft"
            ):
                show_empty_location = True
            sale.show_empty_location = show_empty_location

    def button_empty_location(self):
        self.ensure_one()
        if self.order_line:
            self.order_line.unlink()
        if not self.type_id:
            raise ValidationError(_("The sale must have type."))
        if not self.type_id.picking_type_id:
            raise ValidationError(_("The sale type must have picking type."))
        if not self.type_id.picking_type_id.default_location_src_id:
            raise ValidationError(_("The picking type must have source location."))
        if not self.state == "draft":
            raise ValidationError(_("The sale must be in draft."))
        if self.type_id.picking_type_id.default_location_src_id:
            stock = self.env["stock.quant"].search(
                [
                    (
                        "location_id",
                        "=",
                        self.type_id.picking_type_id.default_location_src_id.id,
                    )
                ]
            )
            for line in stock:
                if line.quantity > 0:
                    sale_line_obj = self.env["sale.order.line"]
                    vals = {
                        "product_id": line.product_id.id,
                        "lot_id": line.lot_id.id,
                        "product_uom_qty": line.available_quantity,
                        "product_uom": line.product_uom_id.id,
                        "order_id": self.id,
                    }
                    sale_line = sale_line_obj.new(vals)
                    for comp_onchange in sale_line._onchange_methods[
                        "product_id",
                        "lot_id",
                        "product_uom_quantity",
                        "product_uom",
                        "sale_id",
                    ]:
                        comp_onchange(sale_line)
                    vals = sale_line._convert_to_write(sale_line._cache)
                    sale_line_obj.create(vals)
