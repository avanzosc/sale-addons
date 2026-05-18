# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    special_partner_id = fields.Many2one(
        string="Special Partner",
        comodel_name="res.partner",
        compute="_compute_special_partner_id",
        store=True,
    )

    @api.depends("order_id", "order_id.special_burden", "order_id.partner_id")
    def _compute_special_partner_id(self):
        for line in self:
            partner = False
            if (
                line.order_id
                and line.order_id.special_burden
                and (line.order_id.partner_id)
            ):
                partner = line.order_id.partner_id.id
            line.special_partner_id = partner

    def action_create_burden_picking(self):
        burden_type = []
        for line in self:
            if line.order_id and not line.order_id.type_id:
                raise ValidationError(_("The sale order has not type."))
            if (
                line.order_id
                and line.order_id.type_id
                and not (line.order_id.type_id.burden_picking_type)
            ):
                raise ValidationError(
                    _("The sale order type has not burden picking type.")
                )
            if not line.order_id.type_id.burden_picking_type.default_location_src_id:
                raise ValidationError(
                    _("The burden picking type has not source location.")
                )
            if not line.order_id.type_id.burden_picking_type.default_location_dest_id:
                raise ValidationError(
                    _("The burden picking type has not destination location.")
                )
            if line.order_id.type_id.burden_picking_type not in burden_type:
                burden_picking_type = line.order_id.type_id.burden_picking_type
                burden_type.append(burden_picking_type)
                picking = self.env["stock.picking"].create(
                    {
                        "picking_type_id": burden_picking_type.id,
                        "location_id": (burden_picking_type.default_location_src_id.id),
                        "location_dest_id": (
                            burden_picking_type.default_location_dest_id.id
                        ),
                        "custom_date_done": fields.Datetime.now(),
                        "user_id": self.env.user.id,
                        "company_id": line.company_id.id,
                    }
                )
                processed = self.env["sale.order.line"]
                same_type_lines = self.filtered(
                    lambda c, bpt=burden_picking_type: (
                        c.order_id.type_id.burden_picking_type == bpt
                    )
                )
                for same_type_line in same_type_lines:
                    if same_type_line.order_id.special_burden:
                        self._create_burden_move(
                            picking,
                            same_type_line.product_id,
                            same_type_line.product_packaging_id,
                            same_type_line.product_packaging_qty,
                            same_type_line.special_partner_id,
                            same_type_line.surplus,
                        )
                    elif same_type_line not in processed:
                        same_product_package = same_type_lines.filtered(
                            lambda c, stl=same_type_line: (
                                c.product_id == stl.product_id
                                and c.product_packaging_id == stl.product_packaging_id
                                and not c.order_id.special_burden
                                and c.surplus == stl.surplus
                            )
                        )
                        self._create_burden_move(
                            picking,
                            same_type_line.product_id,
                            same_type_line.product_packaging_id,
                            sum(same_product_package.mapped("product_packaging_qty")),
                            same_type_line.special_partner_id,
                            same_type_line.surplus,
                        )
                        processed |= same_product_package

    def _create_burden_move(
        self,
        picking,
        product,
        packaging,
        packaging_qty,
        burden_partner,
        surplus,
    ):
        if packaging and packaging_qty:
            product_uom_qty = packaging.qty * packaging_qty
        else:
            product_uom_qty = packaging_qty or 0.0
        move = self.env["stock.move"].create(
            {
                "name": product.display_name,
                "picking_id": picking.id,
                "product_id": product.id,
                "product_uom": product.uom_id.id,
                "product_uom_qty": product_uom_qty,
                "product_packaging_id": packaging.id if packaging else False,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
                "company_id": picking.company_id.id,
            }
        )
        self.env["stock.move.line"].create(
            {
                "move_id": move.id,
                "picking_id": picking.id,
                "product_id": product.id,
                "product_uom_id": product.uom_id.id,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
                "quantity": product_uom_qty,
                "burden_partner_id": burden_partner.id if burden_partner else False,
                "surplus": surplus,
                "company_id": picking.company_id.id,
            }
        )
        return move
