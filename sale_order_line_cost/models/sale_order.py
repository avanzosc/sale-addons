# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_cost = fields.Float(
        string='Total Cost', compute='_compute_total_cost', store=True)

    @api.depends('order_line', 'order_line.cost_subtotal')
    def _compute_total_cost(self):
        for line in self:
            line.total_cost = sum(line.order_line.mapped('cost_subtotal'))
