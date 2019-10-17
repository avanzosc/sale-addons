# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleStockAnalytic(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleStockAnalytic, cls).setUpClass()
        cls.env.user.company_id.autocreate_sale_analytic_account = True
        cls.product = cls.env.ref('product.consu_delivery_01')
        sale_vals = {
            'name': 'Sale for test sale_stock_analytic',
            'partner_id': cls.env.ref('base.res_partner_12').id}
        line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100}
        sale_vals['order_line'] = [(0, 0, line_vals)]
        cls.sale = cls.env['sale.order'].create(sale_vals)

    def test_sale_stock_analytic(self):
        self.assertFalse(self.sale.analytic_account_id)
        self.sale.action_confirm()
        self.assertTrue(self.sale.analytic_account_id)
        self.assertEqual(
            self.sale.analytic_account_id,
            self.sale.picking_ids[0].analytic_account_id)
