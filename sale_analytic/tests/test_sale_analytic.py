# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSaleAnalytic(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleAnalytic, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.sale_model = cls.env['sale.order'].\
            with_context(tracking_disable=True)
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'type': 'product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })

    def test_sale_analytic(self):
        sale_data = {
            'partner_id': self.partner.id,
            'partner_invoice_id': self.partner.id,
            'partner_shipping_id': self.partner.id,
        }
        self.sale_order1 = self.sale_model.create(sale_data)
        sale_line_data = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'price_unit': 100,
            'order_id': self.sale_order1.id
        }
        self.env['sale.order.line'].create(sale_line_data)
        self.sale_order1.action_confirm()
        self.assertEqual(len(self.sale_order1.analytic_account_id), 0)
        self.sale_order2 = self.sale_order1.copy()
        self.sale_order2.company_id.autocreate_sale_analytic_account = True
        self.sale_order2.action_confirm()
        self.assertEqual(len(self.sale_order2.analytic_account_id), 1)
