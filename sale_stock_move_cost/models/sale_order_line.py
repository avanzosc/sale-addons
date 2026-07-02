# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_line_cost = fields.Float(
        string="Line Cost",
        digits="Product Price",
        copy=False,
        store=True,
        compute="_compute_sale_line_cost_margin",
    )
    sale_line_margin = fields.Float(
        string="Line Margin",
        digits="Product Price",
        copy=False,
        store=True,
        compute="_compute_sale_line_cost_margin",
    )

    @api.depends("move_ids", "move_ids.move_line_ids", "move_ids.move_line_ids.cost")
    def _compute_sale_line_cost_margin(self):
        for line in self:
            sale_line_cost = 0
            sale_line_margin = 0
            moves = line.move_ids.filtered(lambda x: x.state != "cancel")
            for move in moves:
                sale_line_cost += sum(move.move_line_ids.mapped("cost"))
            if sale_line_cost > 0:
                sale_line_margin = line.price_subtotal - sale_line_cost
            line.sale_line_cost = sale_line_cost
            line.sale_line_margin = sale_line_margin
