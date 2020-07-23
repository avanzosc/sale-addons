# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_line_cost = fields.Monetary(
        string='Total line cost', copy=False,
        compute='_compute_sale_order_lines_cost', store=True)

    @api.multi
    @api.depends('order_line', 'order_line.cost')
    def _compute_sale_order_lines_cost(self):
        for sale in self.filtered("order_line"):
            sale.total_line_cost = sum(sale.mapped("order_line.cost"))
