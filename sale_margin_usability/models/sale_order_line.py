# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    total_cost = fields.Float(
        string="Total Cost", compute="_compute_total_cost",
        digits="Product Price", store=True, readonly=False,
        groups="base.group_user")

    @api.depends("product_uom_qty", "purchase_price")
    def _compute_total_cost(self):
        for line in self:
            line.total_cost = line.product_uom_qty * line.purchase_price
