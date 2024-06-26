# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_sale_order_line_data(self, purchase_line, dest_company, sale_order):
        result = super(PurchaseOrder, self)._prepare_sale_order_line_data(
            purchase_line, dest_company, sale_order
        )
        if purchase_line.product_packaging:
            result.update(
                {
                    "product_packaging": purchase_line.product_packaging.id,
                    "product_packaging_qty": purchase_line.product_packaging_qty,
                }
            )
        return result
