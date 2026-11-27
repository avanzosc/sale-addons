# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    line_import_ids = fields.One2many(
        comodel_name="sale.order.line.import",
        inverse_name="order_id",
        string="Line Imports",
        copy=False,
    )
    line_import_count = fields.Integer(compute="_compute_line_import_count")

    def _compute_line_import_count(self):
        for order in self:
            order.line_import_count = len(order.line_import_ids)

    def action_new_line_import(self):
        self.ensure_one()
        return {
            "name": _("Import Sale Order Lines"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order.line.import",
            "view_mode": "form",
            "target": "current",
            "context": {"default_order_id": self.id},
        }

    def action_view_line_imports(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale_order_line_import_wizard.sale_order_line_import_action"
        )
        action.update(
            {
                "domain": [("order_id", "=", self.id)],
                "context": {"default_order_id": self.id},
            }
        )
        if len(self.line_import_ids) == 1:
            action.update(
                {"view_mode": "form", "res_id": self.line_import_ids.id, "views": []}
            )
        return action
