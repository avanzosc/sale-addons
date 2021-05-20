# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            return super(SaleOrderLine, self).product_uom_change()
        my_price_unit = self.price_unit
        result = super(SaleOrderLine, self).product_uom_change()
        if my_price_unit:
            self.price_unit = my_price_unit
        return result
