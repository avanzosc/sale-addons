# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
    ):
        res = super()._get_stock_move_values(
            product_id,
            product_qty,
            product_uom,
            location_id,
            name,
            origin,
            company_id,
            values,
        )
        if values.get("sale_line_id", False):
            sale_line = (
                self.env["sale.order.line"].sudo().browse(values.get("sale_line_id"))
            )
            picking_type = (
                sale_line.order_id.type_id
                and sale_line.order_id.type_id.picking_type_id
            )
            if picking_type:
                res.update(
                    {
                        "picking_type_id": picking_type.id
                        or res.get("picking_type_id"),
                        "location_id": picking_type.default_location_src_id.id
                        or res.get("location_id"),
                        "location_dest_id": picking_type.default_location_dest_id.id
                        or res.get("location_dest_id"),
                    }
                )
                if picking_type.sequence_id:
                    res["sequence"] = picking_type.sequence_id.id
        return res
