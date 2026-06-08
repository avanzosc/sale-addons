# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_uom_qty")
    def _onchange_product_uom_qty(self):
        # Keep parent onchange behavior and suppress quantity decrease warnings.
        parent_onchange = getattr(super(), "_onchange_product_uom_qty", None)
        result = parent_onchange() if parent_onchange else {}
        if isinstance(result, dict) and "warning" in result:
            result["warning"] = []
        return result or {}

    def write(self, values):
        lines = self.env["sale.order.line"]
        if "product_uom_qty" in values:
            precision = self.env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )
            lines = self.filtered(
                lambda line: line.state == "sale"
                and not line.is_expense
                and float_compare(
                    line.product_uom_qty,
                    values["product_uom_qty"],
                    precision_digits=precision,
                )
                == 1
            )

        old_packaging = {line: line.product_packaging_id for line in self}
        previous_product_uom_qty = {line.id: line.product_uom_qty for line in lines}

        result = super().write(values)

        for line in self:
            if line.product_packaging_id != old_packaging[line]:
                line.move_ids.filtered(
                    lambda move: move.state not in ["cancel", "done"]
                ).product_packaging_id = line.product_packaging_id

        if lines:
            lines._action_launch_stock_rule(
                previous_product_uom_qty=previous_product_uom_qty
            )
        return result
