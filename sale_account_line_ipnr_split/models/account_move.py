# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models
from odoo.exceptions import UserError

INVOICE_TYPES = ("out_invoice", "out_refund", "in_invoice", "in_refund")


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_ipnr_rounding(self):
        digits = int(
            self.env["ir.config_parameter"].sudo().get_param("ipnr.rounding_digits")
        )
        return digits if digits else 0

    def _get_ipnr_product(self):
        product_id = self.env["ir.config_parameter"].sudo().get_param("ipnr.product_id")
        if not product_id:
            raise UserError(
                _(
                    "IPNR product not configured. Please set it in Sales Settings → IPNR."
                )
            )
        product = self.env["product.product"].browse(int(product_id))
        if not product.exists():
            raise UserError(
                _(
                    "The configured IPNR product no longer exists."
                    " Please update it in Sales Settings → IPNR."
                )
            )
        return product

    def _get_ipnr_rate(self):
        report = self.env["l10n.es.aeat.mod592.report"].search([], limit=1)
        if not report:
            raise UserError(
                _(
                    "No record found in l10n.es.aeat.mod592.report. "
                    "Cannot read amount_plastic_tax."
                )
            )
        rate = report.amount_plastic_tax or 0.0
        if rate <= 0:
            raise UserError(
                f"Invalid amount_plastic_tax (must be > 0) on "
                f"l10n.es.aeat.mod592.report. Current: {rate}"
            )
        return rate

    def _assert_invoice_type(self):
        if self.move_type not in INVOICE_TYPES:
            raise UserError(
                f"This action is only allowed for invoices/refunds "
                f"({', '.join(INVOICE_TYPES)}). Current type: {self.move_type}"
            )

    def _assert_draft_state(self, action="perform this action"):
        if self.state != "draft":
            raise UserError(
                f"Move must be in draft to {action}. Current state: {self.state}"
            )

    def _is_regular_line(self, line):
        return (
            line.display_type not in ("line_section", "line_note") and line.product_id
        )

    def _remove_ipnr_lines(self, ipnr_product):
        self.invoice_line_ids.filtered(
            lambda line: self._is_regular_line(line) and line.product_id == ipnr_product
        ).unlink()

    def _source_lines(self, ipnr_product):
        return self.invoice_line_ids.filtered(
            lambda line: self._is_regular_line(line) and line.product_id != ipnr_product
        ).sorted(key=lambda line: (line.sequence, line.id))

    def _find_sale_parent_line(self, invoice_line, ipnr_product):
        for sale_line in invoice_line.sale_line_ids:
            if sale_line.product_id and sale_line.product_id != ipnr_product:
                return sale_line
        return None

    def _sync_gross_from_so(self, source_lines, ipnr_product, rounding):
        for line in source_lines:
            if line.x_ipnr_gross_price_unit:
                continue
            sale_parent = self._find_sale_parent_line(line, ipnr_product)
            if sale_parent and sale_parent.x_ipnr_gross_price_unit:
                line.write(
                    {
                        "x_ipnr_gross_price_unit": round(
                            sale_parent.x_ipnr_gross_price_unit, rounding
                        )
                    }
                )

    def _resequence_lines(self, source_lines):
        for seq, line in enumerate(source_lines, start=1):
            new_seq = seq * 10
            if line.sequence != new_seq:
                line.write({"sequence": new_seq})

    def action_ipnr_split(self):
        self.ensure_one()

        ipnr_product = self._get_ipnr_product()
        rounding = self._get_ipnr_rounding()

        rate = self._get_ipnr_rate()
        self._assert_invoice_type()
        self._assert_draft_state("split IPNR")
        self._remove_ipnr_lines(ipnr_product)

        source_lines = self._source_lines(ipnr_product)
        self._sync_gross_from_so(source_lines, ipnr_product, rounding)
        self._resequence_lines(source_lines)

        new_ipnr_lines = []

        for line in source_lines:
            qty = line.quantity or 0.0
            if qty <= 0:
                continue

            non_recyclable_kg = line.product_id.plastic_weight_non_recyclable or 0.0
            ipnr_unit_price = round(rate * non_recyclable_kg, rounding)

            if ipnr_unit_price <= 0:
                if line.x_ipnr_gross_price_unit:
                    line.write(
                        {
                            "price_unit": round(line.x_ipnr_gross_price_unit, rounding),
                            "x_ipnr_gross_price_unit": 0.0,
                        }
                    )
                continue

            gross_visible = round(
                line.x_ipnr_gross_price_unit or line.price_unit, rounding
            )

            discount = line.discount or 0.0
            discount_factor = 1.0 - (discount / 100.0)
            if discount_factor <= 0.0:
                raise UserError(
                    f"Line '{line.product_id.display_name}' has 100% discount; "
                    f"cannot split embedded IPNR safely."
                )

            price_after_discount = round(gross_visible * discount_factor, rounding)
            net_after_discount = round(price_after_discount - ipnr_unit_price, rounding)

            if net_after_discount < 0:
                raise UserError(
                    f"Line '{line.product_id.display_name}' results in a negative net "
                    f"(after discount): {price_after_discount:.{rounding}f} - "
                    f"{ipnr_unit_price:.{rounding}f} = {net_after_discount:.{rounding}f}"
                )

            net_visible = round(net_after_discount / discount_factor, rounding)

            line.write(
                {
                    "x_ipnr_gross_price_unit": gross_visible,
                    "price_unit": net_visible,
                }
            )

            ipnr_vals = {
                "sequence": (line.sequence or 0) + 1,
                "product_id": ipnr_product.id,
                "name": f"IPNR ({rate:.2f} €/kg) - {line.name}",
                "quantity": qty,
                "product_uom_id": line.product_uom_id.id,
                "price_unit": ipnr_unit_price,
                "discount": 0.0,
                "tax_ids": [(6, 0, line.tax_ids.ids)],
                "x_ipnr_parent_line_id": line.id,
            }
            if line.account_id:
                ipnr_vals["account_id"] = line.account_id.id
            if line.analytic_distribution:
                ipnr_vals["analytic_distribution"] = line.analytic_distribution

            new_ipnr_lines.append((0, 0, ipnr_vals))

        if new_ipnr_lines:
            self.write({"invoice_line_ids": new_ipnr_lines})

    def action_ipnr_reverse(self):
        self.ensure_one()

        ipnr_product = self._get_ipnr_product()
        rounding = self._get_ipnr_rounding()

        self._assert_invoice_type()
        self._assert_draft_state("revert IPNR split")
        self._remove_ipnr_lines(ipnr_product)

        restored = 0
        copied_from_so = 0

        for line in self._source_lines(ipnr_product):
            gross_saved = line.x_ipnr_gross_price_unit

            if not gross_saved:
                sale_parent = self._find_sale_parent_line(line, ipnr_product)
                if sale_parent and sale_parent.x_ipnr_gross_price_unit:
                    gross_saved = sale_parent.x_ipnr_gross_price_unit
                    line.write(
                        {"x_ipnr_gross_price_unit": round(gross_saved, rounding)}
                    )
                    copied_from_so += 1

            if gross_saved:
                line.write({"price_unit": round(gross_saved, rounding)})
                restored += 1

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "IPNR",
                "message": (
                    f"Revert done. Restored {restored} line(s). "
                    f"Copied gross from SO for {copied_from_so} line(s)."
                ),
                "sticky": False,
            },
        }
