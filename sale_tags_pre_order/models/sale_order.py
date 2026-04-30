# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if any(tag.is_pre_order for tag in order.tag_ids) and (
                order.invoice_status == "no"
                or (
                    order.invoice_status == "to invoice"
                    and (order.shopify_order_status == "unfulfilled")
                )
            ):
                if order.invoice_ids:
                    continue
                wizard = (
                    self.env["sale.advance.payment.inv"]
                    .with_context(
                        active_model="sale.order",
                        active_ids=order.ids,
                        active_id=order.id,
                    )
                    .create(
                        {
                            "advance_payment_method": "percentage",
                            "amount": 100,
                        }
                    )
                )
                wizard.create_invoices()
        return result
