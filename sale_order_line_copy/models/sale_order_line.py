# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def copy_sale_order_line(self):
        for line in self:
            return line.copy(
                {'name': self.name,
                 'order_id': self.order_id.id,
                 'product_id': self.product_id.id,
                 })
