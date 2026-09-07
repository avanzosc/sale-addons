# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            order.create_pre_order_invoice()
        return result

    def create_pre_order_invoice(self):
        self.ensure_one()

        if not any(tag.is_pre_order for tag in self.tag_ids):
            return

        if self._has_active_downpayment_invoice():
            return

        if not (
            self.invoice_status == "no"
            or (
                self.invoice_status == "to invoice"
                and self.shopify_order_status == "unfulfilled"
            )
        ):
            return

        self.create_advance_invoice()

    def create_advance_invoice(self):
        for order in self:
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
            invoice_action = wizard.create_invoices()
            invoice = self.env["account.move"].browse(invoice_action.get("res_id"))
            tag = next((tag for tag in self.tag_ids if tag.is_pre_order), False)
            if tag and tag.journal_id:
                invoice.journal_id = tag.journal_id.id
            if any(tag.invoice_mode in ("open", "paid") for tag in order.tag_ids):
                invoice.action_post()
            if (
                any(tag.invoice_mode == "paid" for tag in order.tag_ids)
                and order.shopify_payment_gateway_id
                and order.shopify_payment_gateway_id.journal_id
            ):
                wizard_model = self.env["account.payment.register"].with_context(
                    active_model="account.move",
                    active_ids=invoice.ids,
                )
                wizard = wizard_model.new(
                    {
                        "journal_id": order.shopify_payment_gateway_id.journal_id.id,
                        "amount": invoice.amount_residual,
                        "payment_date": fields.Date.today(),
                        "communication": invoice.name,
                    }
                )
                wizard._compute_from_lines()
                wizard._compute_payment_method_line_fields()
                wizard._compute_payment_method_line_id()
                vals = wizard._convert_to_write(wizard._cache)
                wizard = wizard_model.create(vals)
                wizard.journal_id = order.shopify_payment_gateway_id.journal_id.id
                wizard.action_create_payments()

    def _has_active_downpayment_invoice(self):
        self.ensure_one()
        downpayment_lines = self.order_line.filtered("is_downpayment")
        invoices = downpayment_lines.invoice_lines.move_id.filtered(
            lambda move: move.state != "cancel"
        )
        return bool(invoices)

    def update_tag_in_shopify_order(self, order, shopify_tags):
        result = super().update_tag_in_shopify_order(
            order,
            shopify_tags,
        )

        if (
            order.state in ("sale", "done")
            and any(tag.is_pre_order for tag in order.tag_ids)
            and not order._has_active_downpayment_invoice()
        ):
            order.create_pre_order_invoice()

        return result
