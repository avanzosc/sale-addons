# Copyright 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSaleOrderLineManualSequence(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderLineManualSequence, cls).setUpClass()
        cls.sale_obj = cls.env['sale.order']
        cls.wiz_obj = cls.env['sale.advance.payment.inv']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner sale order line manual sequence',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product sale order line manual sequence',
            'default_code': 'Psolc',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'product',
            'invoice_policy': 'order',
            'company_id': cls.company.id})
        sale_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100,
            'manual_sequence': '009',
            'company_id': cls.company.id}
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)]}
        cls.sale = cls.sale_obj.create(sale_vals)

    def test_sale_order_line_manual_sequence(self):
        self.sale.action_confirm()
        self.assertEqual(len(self.sale.picking_ids), 1)
        for picking in self.sale.picking_ids:
            for move in picking.move_ids_without_package:
                self.assertEqual(move.manual_sequence, '009')
        wiz = self.wiz_obj.with_context(
            active_ids=[self.sale.id]).create(
                {'advance_payment_method': 'delivered'})
        wiz.with_context(active_ids=[self.sale.id]).create_invoices()
        self.assertEqual(len(self.sale.invoice_ids), 1)
