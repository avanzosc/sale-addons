# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderLineKeepPriceUnit(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderLineKeepPriceUnit, cls).setUpClass()
        cls.sale_obj = cls.env['sale.order']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner sale order line keep price unit',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product sale order line contract',
            'default_code': 'Psolc',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'recurring_rule_type': 'monthly',
            'recurring_interval': 1})
        sale_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100}
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)]}
        cls.sale = cls.sale_obj.create(sale_vals)

    def test_sale_order_line_keep_price_unit(self):
        self.sale.order_line[0].product_uom_qty = 2
        self.sale.order_line[0].product_uom_change()
        self.assertEquals(self.sale.order_line[0].price_unit, 100)
