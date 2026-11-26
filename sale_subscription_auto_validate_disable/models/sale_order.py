from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _process_auto_invoice(self, invoice):
        if self.env.context.get("recurring_automatic") and not self.mapped(
            "payment_token_id"
        ):
            invoice.write(
                {
                    "subscription_auto_validate_draft": True,
                }
            )
            return
        return super()._process_auto_invoice(invoice)
