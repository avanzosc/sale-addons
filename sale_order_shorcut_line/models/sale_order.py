# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_line_count = fields.Integer(
        string="# Sale line", compute="_compute_sale_line_count"
    )

    def _compute_sale_line_count(self):
        for line in self:
            line.sale_line_count = len(line.order_line)

    def action_view_sale_lines(self):
        self.ensure_one()
        self.action_put_section_in_lines()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_order_line_input.action_sales_order_line_input"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.order_line.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        action["context"] = dict(self._context, create=False, default_order_id=self.id)
        return action

    def action_create_purchase_order_for_service(self):
        for sale in self:
            lines = sale.order_line.filtered(
                lambda x: x.product_supplier_id and not x.purchase_id
            )
            for line in lines:
                line.create_purchase_order_for_service()

    def action_put_section_in_lines(self):
        for sale in self:
            section_lines = sale.order_line.filtered(
                lambda x: x.display_type == "line_section"
            )
            for section_line in section_lines:
                section_line.section_line_id = section_line.id
                lines = sale.order_line.filtered(
                    lambda z: z.sequence > section_line.sequence
                )
                for line in lines:
                    if line.display_type == "line_section":
                        break
                    line.section_line_id = section_line.id
