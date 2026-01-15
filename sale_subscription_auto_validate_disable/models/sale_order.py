from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def validate_and_send_invoice(self, auto_commit=False, invoice=None, **kwargs):
        """Force manual validation by disabling the auto-commit flag."""
        if invoice is None and auto_commit and not isinstance(auto_commit, bool):
            invoice = auto_commit
        return super().validate_and_send_invoice(False, invoice, **kwargs)

    @api.model
    def _cron_recurring_create_invoice(self):
        return self._create_recurring_invoice(automatic=False)
