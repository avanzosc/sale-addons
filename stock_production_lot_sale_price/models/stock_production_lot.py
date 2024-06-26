# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    sale_price = fields.Float(string="Sale Price", compute="_compute_sale_price")

    def _compute_sale_price(self):
        for lot in self:
            price = 0
            lines = self.env["stock.move.line"].search(
                [
                    ("lot_id", "=", lot.id),
                    ("picking_code", "=", "outgoing"),
                    ("state", "=", "done"),
                ]
            )
            if lines:
                price = sum(lines.mapped("amount")) / sum(lines.mapped("qty_done"))
            lot.sale_price = price
