# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("product_id")
    def _compute_name(self):
        result = super()._compute_name()
        for line in self:
            cond = [
                ("partner_id", "=", line.order_id.partner_id.id),
                ("template_id", "=", line.product_id.product_tmpl_id.id),
            ]
            product_code = self.env["product.template.customer.code"].search(
                cond, limit=1
            )
            if product_code:
                line.name = ("[%(product_code)s]-%(line_name)s") % {
                    "product_code": product_code.customer_code,
                    "line_name": line.name,
                }
        return result
