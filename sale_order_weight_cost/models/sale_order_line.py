# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weight = fields.Float(
        string='Weight', digits_compute=dp.get_precision('Stock Weight'))
    cost = fields.Float(
        string='Cost', digits_compute=dp.get_precision('Product Price'))

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        self.weight = self.product_id.weight
        self.cost = self.product_id.standard_price
        return res
