# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "order_id.type_id.filter_lot_by_location",
        "order_id.type_id.picking_type_id",
        "order_id.type_id.picking_type_id.default_location_src_id",
    )
    def _compute_domain_lot_id(self):
        location_filtered = self.filtered(
            lambda line: line.product_id
            and line.product_id.tracking != "none"
            and line.order_id.type_id.filter_lot_by_location
        )
        res = super(SaleOrderLine, self - location_filtered)._compute_domain_lot_id()
        if not location_filtered:
            return res
        for line in location_filtered:
            pick_type = line.order_id.type_id.picking_type_id
            if not pick_type:
                raise ValidationError(
                    _("The order type does not have the picking type.")
                )
            if not pick_type.default_location_src_id:
                raise ValidationError(
                    _("The picking type does not have the source location.")
                )
            quants = self.env["stock.quant"].search(
                [
                    ("product_id", "=", line.product_id.id),
                    ("company_id", "=", line.company_id.id),
                    ("location_id", "=", pick_type.default_location_src_id.id),
                ]
            )
            lot_ids = quants.filtered(lambda q: q.quantity > 0).mapped("lot_id")
            line.domain_lot_id = [("id", "in", lot_ids.ids)]
