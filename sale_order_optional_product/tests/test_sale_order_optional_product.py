# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSaleOrderOptionalProduct(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderOptionalProduct, cls).setUpClass()
        cls.product_obj = cls.env['product.product']
        cls.product = cls.product_obj.create({
            'name': 'aaa',
            'sale_line_warn': 'warning',
            'sale_line_warn_msg': 'There is a warning',
            'list_price': 10,
        })
        cls.sale_obj = cls.env['sale.order']
        cls.optional_product_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'price_unit': cls.product.list_price,
            'uom_id': cls.product.uom_id.id}
        cls.sale = cls.sale_obj.create({
            'partner_id': cls.env['res.partner'].search([], limit=1).id})
        cls.sale.sale_order_option_ids = [
            (0, 0, cls.optional_product_vals)]

    def test_sale_order_optional_product(self):
        result = self.sale.sale_order_option_ids[0].button_add_to_order()
        self.assertEqual(result['warning']['message'], 'There is a warning')
