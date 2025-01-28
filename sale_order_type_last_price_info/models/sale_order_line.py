# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def product_id_change(self):
        result = super().product_id_change()
        vals = {}
        if (
            self.product_id
            and self.order_id
            and self.order_id.type_id
            and (self.order_id.type_id.sale_price_type == "sale")
        ):
            vals["price_unit"] = self.sale_last_price_unit
        if (
            self.product_id
            and self.order_id
            and self.order_id.type_id
            and (self.order_id.type_id.sale_price_type == "invoice")
        ):
            vals["price_unit"] = self.invoice_last_price_unit
        self.update(vals)
        return result

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        result = super().product_uom_change()
        if (
            self.product_id
            and self.order_id
            and self.order_id.type_id
            and (self.order_id.type_id.sale_price_type == "sale")
        ):
            self.price_unit = self.sale_last_price_unit
        if (
            self.product_id
            and self.order_id
            and self.order_id.type_id
            and (self.order_id.type_id.sale_price_type == "invoice")
        ):
            self.price_unit = self.invoice_last_price_unit
        return result
