# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_view_products_stock_forecast_from_sale(self):
        res = super(
            SaleOrder, self).action_view_products_stock_forecast_from_sale()
        if (self.expected_delivery_date and self.expected_end_date and
                res.get('domain', False)):
            cond = [('product_id', 'in', self.sale_product_ids.ids),
                    ('date', '>=', self.expected_delivery_date),
                    ('date', '<=', self.expected_end_date)]
            res['domain'] = cond
        return res
