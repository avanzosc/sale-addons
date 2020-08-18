# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class ProductProductStockForecast(models.Model):
    _inherit = 'product.product.stock.forecast'

    def _catch_max_fec_for_calc_qty_per_day(self, moves):
        date_expected = super(
            ProductProductStockForecast,
            self)._catch_max_fec_for_calc_qty_per_day(moves)
        cond = [('expected_end_date', '!=', False)]
        sales = self.env['sale.order'].search(cond)
        if sales:
            sale = max(sales, key=lambda x: x.expected_end_date)
            if sale.expected_end_date > date_expected:
                return sale.expected_end_date
        return date_expected
