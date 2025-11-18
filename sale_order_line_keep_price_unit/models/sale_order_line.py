# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom', 'product_uom_qty')
    def _onchange_keep_price_unit(self):
        for line in self:
            if not line.product_id or not line.product_uom:
                continue
            if line.technical_price_unit == line.price_unit:
                line.technical_price_unit = line.price_unit + 1e-7
