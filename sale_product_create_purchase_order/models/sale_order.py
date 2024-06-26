# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_create_purchase_order_for_product(self):
        for sale in self:
            lines = sale.order_line.filtered(
                lambda x: x.product_supplier_id and not x.purchase_id
            )
            for line in lines:
                line.create_purchase_order_for_product()
