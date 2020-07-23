# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderWeightCost(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderWeightCost, cls).setUpClass()
        cls.product = cls.env.ref('product.product_product_4d')
        cls.product.write({
            'weight': 1.23,
            'standard_price': 8.75})
        cls.sale = cls.env['sale.order'].search([], limit=1)
        cls.weight_uom = cls.env[
            'product.template']._get_weight_uom_id_from_ir_config_parameter()

    def test_sale_order_weight_cost(self):
        self.sale.order_line[0].write({
            'product_id': self.product.id})
        self.sale.order_line[0].product_id_change()
        self.assertEqual(
            self.sale.order_line[0].weight, 1.23)
        self.assertEqual(
            self.sale.order_line[0].cost, 8.75)
        self.assertEqual(
            self.sale.order_line[0].weight_uom_id, self.weight_uom)
        self.assertEqual(
            self.sale.total_line_cost, sum(
                self.sale.mapped("order_line.cost")))
