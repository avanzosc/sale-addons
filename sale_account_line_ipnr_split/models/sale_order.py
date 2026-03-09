# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

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

    def _assert_quotation_state(self):
        if self.state not in ("draft", "sent"):
            raise UserError(
                f"Order {self.name} is not in quotation/sent state. "
                f"Current state: {self.state}"
            )

    def _is_regular_line(self, line):
        return (
            line.display_type not in ("line_section", "line_note") and line.product_id
        )

    def _remove_ipnr_lines(self, ipnr_product):
        self.order_line.filtered(
            lambda line: self._is_regular_line(line) and line.product_id == ipnr_product
        ).unlink()

    def _source_lines(self, ipnr_product):
        return self.order_line.filtered(
            lambda line: self._is_regular_line(line) and line.product_id != ipnr_product
        ).sorted(key=lambda line: (line.sequence, line.id))

    def action_ipnr_split(self):
        self.ensure_one()

        ipnr_product = self._get_ipnr_product()
        rounding = self._get_ipnr_rounding()

        rate = self._get_ipnr_rate()
        self._assert_quotation_state()
        self._remove_ipnr_lines(ipnr_product)

        new_ipnr_lines = []

        for line in self._source_lines(ipnr_product):
            qty = line.product_uom_qty or 0.0
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

            discount = line.discount or 0.0
            discount_factor = 1.0 - (discount / 100.0)
            if discount_factor <= 0.0:
                raise UserError(
                    f"Line '{line.product_id.display_name}' has 100% discount; "
                    f"cannot split embedded IPNR safely."
                )

            gross_visible = round(
                line.x_ipnr_gross_price_unit or line.price_unit, rounding
            )
            price_after_discount = round(gross_visible * discount_factor, rounding)
            net_after_discount = round(price_after_discount - ipnr_unit_price, rounding)

            if net_after_discount < 0:
                raise UserError(
                    f"Line '{line.product_id.display_name}' results in a negative net "
                    f"(after discount): {price_after_discount:.{rounding}f} - "
                    f"{ipnr_unit_price:.{rounding}f} = {net_after_discount:.{rounding}f}"
                )

            new_price_unit = round(net_after_discount / discount_factor, rounding)
            line.write(
                {
                    "x_ipnr_gross_price_unit": gross_visible,
                    "price_unit": new_price_unit,
                }
            )

            ipnr_vals = {
                "sequence": line.sequence or 0,
                "product_id": ipnr_product.id,
                "name": f"IPNR ({rate:.2f} €/kg) - {line.name}",
                "product_uom_qty": qty,
                "product_uom": line.product_uom.id,
                "price_unit": ipnr_unit_price,
                "discount": 0.0,
                "x_ipnr_parent_line_id": line.id,
            }
            if "tax_id" in line._fields:
                ipnr_vals["tax_id"] = [(6, 0, line.tax_id.ids)]

            new_ipnr_lines.append((0, 0, ipnr_vals))

        if new_ipnr_lines:
            self.write({"order_line": new_ipnr_lines})

        self._resequence_lines(ipnr_product)

    def action_ipnr_reverse(self):
        self.ensure_one()

        ipnr_product = self._get_ipnr_product()
        rounding = self._get_ipnr_rounding()

        self._assert_quotation_state()
        self._remove_ipnr_lines(ipnr_product)

        for line in self._source_lines(ipnr_product):
            if not line.x_ipnr_gross_price_unit:
                continue
            line.write({"price_unit": round(line.x_ipnr_gross_price_unit, rounding)})

    def _resequence_lines(self, ipnr_product):
        lines = self.order_line.sorted(key=lambda line: (line.sequence, line.id))
        ipnr_by_parent = {}
        for line in lines:
            if line.product_id == ipnr_product:
                parent = line.x_ipnr_parent_line_id
                if parent:
                    ipnr_by_parent.setdefault(parent.id, []).append(line)
        base_lines = [line for line in lines if line.product_id != ipnr_product]
        ordered = []
        for base in base_lines:
            ordered.append(base)
            ordered.extend(sorted(ipnr_by_parent.get(base.id, []), key=lambda x: x.id))
        for seq, line in enumerate(ordered, start=1):
            new_seq = seq * 10
            if line.sequence != new_seq:
                line.write({"sequence": new_seq})
