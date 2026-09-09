# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id", "linked_line_id", "linked_line_ids")
    def _compute_name(self):
        result = super()._compute_name()
        for line in self.filtered(
            lambda z: z.product_id
            and z.product_id.no_product_description_to_sale_invoice_lines
        ):
            if line.product_id.display_name in line.name:
                line.name = line.name.replace(line.product_id.display_name, "").strip()
        return result
