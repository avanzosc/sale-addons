# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import TransactionCase


class TestSaleOrderWeightCost(TransactionCase):

    def setUp(self):
        super(TestSaleOrderWeightCost, self).setUp()
        self.product = self.browse_ref('product.product_product_4d')
        self.product.write({
            'weight': 1.23,
            'standard_price': 8.75})
        self.sale = self.env['sale.order'].search([], limit=1)

    def test_sale_oprder_weight_cost(self):
        self.sale.order_line[0].write({
            'product_id': self.product.id})
        self.sale.order_line[0].product_id_change()
        self.assertEqual(
            self.sale.order_line[0].weight, 1.23)
        self.assertEqual(
            self.sale.order_line[0].cost, 8.75)
