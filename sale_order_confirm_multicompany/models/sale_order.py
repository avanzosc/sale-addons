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
                    purchase_line = line.auto_purchase_line_id.sudo()
                    purchase_line.write(
                        {
                            "product_packaging_id": line.product_packaging_id.id,
                            "product_packaging_qty": line.product_packaging_qty,
                            "price_unit": line.price_unit,
                            "product_qty": line.product_uom_qty,
                            "no_create_picking": True,
                        }
                    )
                    # Si qty no cambió, _create_or_update_picking no se llamó
                    # y el flag quedó sin resetear
                    if purchase_line.no_create_picking:
                        purchase_line.no_create_picking = False
        return result
