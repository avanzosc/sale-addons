# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tracking = fields.Selection(
        string="Tracking", related="product_id.tracking", store=True
    )
    possible_lot_ids = fields.One2many(
        comodel_name="stock.production.lot", compute="_compute_possible_lot_ids"
    )

    @api.depends(
        "product_id",
        "order_id.type_id",
        "order_id.type_id.picking_type_id",
        "order_id.type_id.filter_lot_by_location",
        "order_id.type_id.picking_type_id.default_location_src_id",
    )
    def _compute_possible_lot_ids(self):
        for line in self:
            lot_ids = self.env["stock.production.lot"]
            if line.product_id and line.product_id.tracking != "none":
                if (
                    line.order_id
                    and line.order_id.type_id
                    and line.order_id.type_id.filter_lot_by_location
                ):
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
                    for quant in quants:
                        qty = quant.quantity
                        if qty > 0:
                            lot_ids += quant.mapped("lot_id")
                else:
                    lots = self.env["stock.production.lot"].search(
                        [
                            ("product_id", "=", line.product_id.id),
                            ("company_id", "=", line.company_id.id),
                        ]
                    )
                    lot_ids += lots
            if lot_ids:
                line.possible_lot_ids = [(6, 0, lot_ids.ids)]
            else:
                line.possible_lot_ids = False

    @api.onchange("product_id")
    def _onchange_product_id_set_lot_domain(self):
        super()._onchange_product_id_set_lot_domain()
