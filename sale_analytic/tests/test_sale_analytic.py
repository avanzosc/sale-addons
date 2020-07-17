# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleAnalytic(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleAnalytic, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.sale_model = cls.env['sale.order'].\
            with_context(tracking_disable=True)
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
            'user_id': cls.env.ref('base.user_admin').id,
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })

    def test_sale_analytic(self):
        new_sale = self.sale_model.new({
            "partner_id": self.partner.id,
            "partner_invoice_id": self.partner.id,
            "partner_shipping_id": self.partner.id,
            "company_id": self.company.id,
        })
        for onchange_method in new_sale._onchange_methods["partner_id"]:
            onchange_method(new_sale)
        sale_data = new_sale._convert_to_write(new_sale._cache)
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
        self.assertEquals(len(self.sale_order1.analytic_account_id), 0)
        self.sale_order2 = self.sale_order1.copy()
        self.assertEquals(self.sale_order2.company_id, self.company)
        self.company.autocreate_sale_analytic_account = True
        self.sale_order2.action_confirm()
        self.assertEquals(self.sale_order2.user_id, self.partner.user_id)
        self.assertEquals(len(self.sale_order2.analytic_account_id), 1)
        analytic_account = self.sale_order2.analytic_account_id[:1]
        self.assertTrue(analytic_account.user_id)
        self.assertEquals(analytic_account.user_id, self.sale_order2.user_id)
        self.assertEquals(
            analytic_account.user_id, analytic_account.partner_id.user_id)
