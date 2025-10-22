# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        result = super().product_id_change()
        self._compute_last_price_unit()
        return result

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        result = super().product_uom_change()
        self._update_price_unit_from_last_price()
        return result

    @api.onchange("sale_last_price_unit", "invoice_last_price_unit")
    def last_price_change(self):
        self._update_price_unit_from_last_price()

    def write(self, vals):
        res = super().write(vals)
        if any(
            field in vals
            for field in ["sale_last_price_unit", "invoice_last_price_unit"]
        ):
            self._update_price_unit_from_last_price()
        return res

    def _update_price_unit_from_last_price(self):
        for line in self:
            if line.product_id and line.order_id and line.order_id.type_id:
                if line.order_id.type_id.sale_price_type == "sale":
                    line.price_unit = line.sale_last_price_unit
                elif line.order_id.type_id.sale_price_type == "invoice":
                    line.price_unit = line.invoice_last_price_unit
