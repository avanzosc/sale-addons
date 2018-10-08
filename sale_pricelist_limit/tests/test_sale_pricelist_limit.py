# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import UserError


class TestSalePricelistLimit(common.TransactionCase):

    def setUp(self):
        super(TestSalePricelistLimit, self).setUp()
        self.sale_order_model = self.env['sale.order']
        product_obj = self.env['product.product']
        self.partner_model = self.env['res.partner']
        self.partner1 = self.partner_model.create({
            'name': 'Partner1',
            'street': 'test_street',
            'zip': '12345',
            'city': 'test_city',
            })
        self.partner2 = self.partner_model.create({
            'name': 'Partner2',
            })
        self.partner3 = self.env.ref('base.res_partner_1').copy(
            {'name': 'Test partner3',
             'ref': 'Test ref3',
             })
        self.product = self.env.ref('product.product_product_2')
        self.product2 = self.env.ref('product.product_product_4')
        self.product3 = product_obj.create(
            {'name': 'Test',
             'type': 'product',
             'default_code': 'A1PT',
             'lst_price': 25})
        self.sale_order1 = self.sale_order_model.create({
            'partner_id': self.partner1.id,
            'order_line': [(0, 0, {'product_id': self.product.id,
                                   'product_uom_qty': 5})],
            })
        self.sale_order2 = self.sale_order_model.create({
            'partner_id': self.partner3.id,
            'order_line': [(0, 0, {'product_id': self.product2.id})],
            })
        self.sale_order3 = self.sale_order_model.create({
            'partner_id': self.partner3.id,
            'order_line': [(0, 0, {'product_id': self.product3.id,
                                   'product_uom_qty': 2})],
            })
        self.test_pricelist = self.partner1.property_product_pricelist.copy(
            {'name': 'Test Pricelist',
             'has_limit': True,
             'limit_amount': 200,
             'limit_qty': 4})
        self.partner1.property_product_pricelist = self.test_pricelist
        self.partner2.property_product_pricelist = self.test_pricelist
        self.partner3.property_product_pricelist = self.test_pricelist

    def test_sale_pricelist_limit(self):
        with self.assertRaises(UserError):
            # Quantity exceeded
            self.sale_order1.action_confirm()
        with self.assertRaises(UserError):
            # Amount exceeded
            self.sale_order2.action_confirm()

    def test_compute_remaining_credit(self):
        self.assertEqual(self.partner3.remain_quantity, 4,
                         'Error, remain quantity does not match ')
        self.sale_order3.action_confirm()
        picking = self.sale_order3.action_view_delivery()
        picking = self.sale_order3.picking_ids[0]
        picking.action_confirm()
        self.partner3._compute_remaining_credit()
        self.assertEqual(self.partner3.remain_quantity, 2,
                         'Error, remain quantity does not match ')
