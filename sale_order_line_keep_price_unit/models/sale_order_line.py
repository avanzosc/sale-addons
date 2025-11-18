# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_uom", "product_uom_qty")
    def _onchange_keep_price_unit(self):
        for line in self:
            if not line.product_id or not line.product_uom:
                continue
            line.technical_price_unit = line.price_unit + 1e-7

    @api.depends("product_id", "product_uom", "product_uom_qty")
    def _compute_price_unit(self):
        manual_lines = self.filtered(
            lambda line: line.technical_price_unit
            and line.technical_price_unit != line.price_unit
        )
        lines_to_compute = self - manual_lines
        if lines_to_compute:
            return super(SaleOrderLine, lines_to_compute)._compute_price_unit()
