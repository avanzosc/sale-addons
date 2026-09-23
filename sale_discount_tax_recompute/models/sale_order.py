# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import Command, _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _recompute_taxes(self):
        discount_data_by_order = {}
        had_reward_lines_by_order = {}

        # Guardamos toda la información ANTES de que estándar
        # recalcule los impuestos.
        for order in self:
            discount_product = order.company_id.sale_discount_product_id

            global_discount_lines = order.order_line.filtered(
                lambda line, discount_product=discount_product: (
                    not line.display_type
                    and not line.is_reward_line
                    and line.product_id == discount_product
                )
            )

            reward_lines = order.order_line.filtered(
                lambda line: not line.display_type and line.is_reward_line
            )

            # Líneas normales utilizadas para inferir cómo cambia
            # cada grupo fiscal con la nueva posición fiscal.
            mapping_lines = (
                order.order_line - global_discount_lines - reward_lines
            ).filtered(
                lambda line: (
                    not line.display_type and line.product_uom_qty and line.price_unit
                )
            )

            discount_data_by_order[order.id] = (
                order._prepare_global_discount_tax_recompute(
                    global_discount_lines,
                    mapping_lines,
                )
            )

            had_reward_lines_by_order[order.id] = bool(reward_lines)

        # Dejamos que Odoo haga primero su recálculo estándar.
        result = super()._recompute_taxes()

        # Corregimos los casos especiales después del recálculo estándar.
        for order in self:
            order._recompute_global_discount_taxes(
                discount_data_by_order.get(order.id, {})
            )

            # Una vez corregidos productos + descuentos globales,
            # regeneramos las líneas de recompensa.
            if had_reward_lines_by_order.get(order.id):
                order._update_programs_and_rewards()

        return result

    def _get_global_discount_taxes(self, line):
        """Return the taxes used by the standard global discount logic."""
        taxes = line.tax_id.flatten_taxes_hierarchy()
        return taxes.filtered(lambda tax: tax.amount_type != "fixed")

    def _get_global_discount_tax_key(self, line):
        """Return a stable key representing the line tax group."""
        taxes = self._get_global_discount_taxes(line)
        return tuple(sorted(taxes.ids))

    def _prepare_global_discount_tax_recompute(
        self,
        discount_lines,
        mapping_lines,
    ):
        """
        Relate each global discount line with the normal lines that
        had the same tax combination before the fiscal position change.
        """
        self.ensure_one()

        lines_by_tax = {}

        for line in mapping_lines:
            key = self._get_global_discount_tax_key(line)

            lines_by_tax.setdefault(
                key,
                self.env["sale.order.line"],
            )
            lines_by_tax[key] |= line

        result = {}

        for discount_line in discount_lines:
            old_tax_key = self._get_global_discount_tax_key(discount_line)

            result[discount_line.id] = lines_by_tax.get(
                old_tax_key,
                self.env["sale.order.line"],
            )

        return result

    def _recompute_global_discount_taxes(self, discount_data):
        self.ensure_one()

        SaleOrderLine = self.env["sale.order.line"]

        for discount_line_id, mapping_lines in discount_data.items():
            discount_line = SaleOrderLine.browse(discount_line_id).exists()

            if not discount_line:
                continue

            if not mapping_lines:
                raise UserError(
                    _(
                        "Could not determine the taxes corresponding "
                        "to the global discount line '%s'."
                    )
                    % discount_line.name
                )

            taxes_by_group = {}

            for line in mapping_lines:
                taxes = self._get_global_discount_taxes(line)
                key = tuple(sorted(taxes.ids))
                taxes_by_group[key] = taxes

            if len(taxes_by_group) != 1:
                raise UserError(
                    _(
                        "The fiscal position change has split one "
                        "global discount tax group into several tax "
                        "groups. Remove and apply the global discount "
                        "again."
                    )
                )

            new_taxes = next(iter(taxes_by_group.values()))

            discount_line.tax_id = [Command.set(new_taxes.ids)]
