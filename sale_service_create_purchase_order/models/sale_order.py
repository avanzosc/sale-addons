# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
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
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_service_create_purchase_order.action_editabable_orders_lines")
        action["domain"] = expression.AND(
            [[("id", "in", self.order_line.ids)],
             safe_eval(action.get("domain") or "[]")]
        )
        action["context"] = dict(
            self._context, create=False, default_order_id=self.id)
        return action

    def action_create_purchase_order_for_service(self):
        for sale in self:
            lines = sale.order_line.filtered(
                lambda x: x.product_supplier_id and not x.purchase_id)
            for line in lines:
                line.create_purchase_order_for_service()
