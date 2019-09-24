# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestSaleStockAnalytic(TransactionCase):

    def setUp(self):
        super(TestSaleStockAnalytic, self).setUp()
        self.product = self.env.ref('product.consu_delivery_01')
        sale_vals = {
            'name': 'Sale for test sale_stock_analytic',
            'partner_id': self.env.ref('base.res_partner_12').id}
        line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 100}
        sale_vals['order_line'] = [(0, 0, line_vals)]
        self.sale = self.env['sale.order'].create(sale_vals)

    def test_sale_stock_analytic(self):
        self.sale.action_confirm()
        self.assertNotEqual(
            self.sale.analytic_account_id, False)
        self.assertEqual(
            self.sale.analytic_account_id,
            self.sale.picking_ids[0].analytic_account_id)
