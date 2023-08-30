# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    count_products = fields.Integer(
        string="Products counter", compute="_compute_count_products")

    def _compute_count_products(self):
        for sale in self:
            counter = 0
            if sale.order_line:
                products = sale.order_line.mapped("product_id")
                counter = len(products)
            sale.count_products = counter

    def action_view_products(self):
        products = self.order_line.mapped("product_id")
        action = self.env.ref("product.product_normal_action")
        action_dict = action and action.read()[0]
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        domain = expression.AND([
            [("id", "in", products.ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict
