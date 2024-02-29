# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizChangeSequenceInSaleLine(models.TransientModel):
    _name = "wiz.change.sequence.in.sale.line"
    _description = "Wizard for change sequence in line"

    sale_line_id = fields.Many2one(
        string="Sale Order Line", comodel_name="sale.order.line",
    )
    actual_sequence = fields.Integer(
        string="Actual Sequence", default=0,
    )
    new_sequence = fields.Integer(
        string="New Sequence", default=0
    )

    @api.model
    def default_get(self, fields):
        result = super(WizChangeSequenceInSaleLine, self).default_get(fields)
        if ("active_model" in self.env.context and
                self.env.context.get("active_model", "aa") == "sale.order.line"):
            line = self.env["sale.order.line"].browse(
                self.env.context.get("active_id"))
            result.update({"sale_line_id": line.id,
                           "actual_sequence": line.sequence})
        return result

    def button_change_sequence(self):
        if self.sale_line_id:
            self.sale_line_id.sequence = self.new_sequence
            return self.sale_line_id.order_id.action_view_sale_lines()
