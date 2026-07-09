# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends("order_id.partner_id", "product_id", "order_id.project_id")
    def _compute_analytic_distribution(self):
        ctx_project = self.env["project.project"].browse(
            self.env.context.get("project_id")
        )
        project_lines = self.filtered(
            lambda line: not line.display_type
            and (
                ctx_project
                or line.product_id.with_company(line.company_id).project_id
                or line.order_id.project_id
            )
        )
        project_lines.write({"analytic_distribution": False})
        return super()._compute_analytic_distribution()
