# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.lot"

    sale_price = fields.Float(compute="_compute_sale_price")

    def _compute_sale_price(self):
        for lot in self:
            price = 0
            total_amount = 0
            total_qty = 0
            lines = self.env["stock.move.line"].search(
                [
                    ("lot_id", "=", lot.id),
                    ("picking_code", "=", "outgoing"),
                    ("state", "=", "done"),
                ]
            )
            if lines:
                for line in lines:
                    qty = line.product_uom_id._compute_quantity(
                        line.quantity, line.product_id.uom_id
                    )
                    if not qty:
                        continue
                    if line.move_id.sale_line_id:
                        unit_price = line.move_id.sale_line_id.price_unit
                    else:
                        unit_price = line.product_id.standard_price
                    total_amount += unit_price * qty
                    total_qty += qty
                if total_qty:
                    price = total_amount / total_qty
            lot.sale_price = price
