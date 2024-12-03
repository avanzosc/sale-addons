# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_sale_lines(self):
        context = self.env.context.copy()
        context.update({"default_order_id": self.id})
        view_tree_id = self.env.ref(
            "sale_order_line_input.view_sales_order_line_input_tree"
        ).id
        return {
            "name": _("Sale Lines"),
            "view_mode": "tree,form",
            "res_model": "sale.order.line",
            "domain": [("id", "in", self.order_line.ids)],
            "views": [(view_tree_id, "tree")],
            "view_id": view_tree_id,
            "type": "ir.actions.act_window",
            "context": context,
        }
