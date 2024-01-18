# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizDuplicateSaleLine(models.TransientModel):
    _name = "wiz.duplicate.sale.line"
    _description = "Wizard for duplicate sale line"

    sale_line_id = fields.Many2one(
        string="Sale Order Line", comodel_name="sale.order.line",
    )

    @api.model
    def default_get(self, fields):
        result = super(WizDuplicateSaleLine, self).default_get(fields)
        if ("active_model" in self.env.context and
                self.env.context.get("active_model", "aa") == "sale.order.line"):
            result.update({"sale_line_id": self.env.context.get("active_id"),})
        return result

    def button_duplicate(self):
        if self.sale_line_id:
            self.sale_line_id.copy({"sequence": self.sale_line_id.sequence})
            return self.sale_line_id.order_id.action_view_sale_lines()
