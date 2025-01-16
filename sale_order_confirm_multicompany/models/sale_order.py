# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def button_confirm_pickings(self):
        result = super().button_confirm_pickings()
        if self.auto_purchase_order_id:
            for line in self.order_line:
                if line.auto_purchase_line_id:
                    line.auto_purchase_line_id.sudo().write(
                        {
                            "product_packaging": line.product_packaging.id,
                            "product_packaging_qty": line.product_packaging_qty,
                            "price_unit": line.price_unit,
                            "price_subtotal": line.price_subtotal,
                            "product_qty": line.product_uom_qty,
                            "no_create_picking": True,
                        }
                    )
        return result
