# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_cost = fields.Monetary(
        string="Total Cost", compute="_compute_total_cost", store=True, readonly=False, groups="base.group_user")

    @api.depends("order_line", "order_line.total_cost")
    def _compute_total_cost(self):
        for sale in self:
            sale.total_cost = sum(sale.order_line.mapped("total_cost"))
