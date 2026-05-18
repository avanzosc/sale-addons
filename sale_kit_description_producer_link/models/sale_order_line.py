# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _set_bom_description(self):
        if not self.product_id or not self.product_id.bom_ids:
            return
        bom = self.env["mrp.bom"].search(
            [
                ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                ("active", "=", True),
            ],
            order="sequence",
            limit=1,
        )
        if not bom:
            return
        lines = [self.product_id.name]
        for line in bom.bom_line_ids:
            text = (
                f"- {line.product_id.name} {line.product_qty}"
                f" {line.product_uom_id.name}"
            )
            extras = [v for v in (line.producer, line.product_link) if v]
            if extras:
                text += ", " + ", ".join(extras)
            lines.append(text)
        self.name = "\n".join(lines)
