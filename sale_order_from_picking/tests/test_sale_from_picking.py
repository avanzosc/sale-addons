# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from openerp import exceptions


class TestSaleFromPicking(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleFromPicking, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.sale_model = cls.env['sale.order']
        cls.picking_model = cls.env['stock.picking']
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.supplier_location = cls.env.ref(
            'stock.stock_location_suppliers').id
        cls.product = cls.product_model.create({
            'name': 'Product',
            'type': 'product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.warehouse1 = cls.env['stock.warehouse'].create({
            'name': 'Base Warehouse',
            'reception_steps': 'one_step',
            'delivery_steps': 'ship_only',
            'code': 'BWH'})

    def test_create_sale_from_picking(self):
        picking_values = {
            'picking_type_id': self.warehouse1.in_type_id.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id,
        }
        self.picking1 = self.picking_model.create(picking_values)
        self.env['stock.move'].create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'picking_id': self.picking1.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id})
        with self.assertRaises(exceptions.Warning):
            # No partner
            self.picking1.create_sale_order()
        self.picking1.partner_id = self.partner
        view_data = self.picking1.create_sale_order()
        self.sale = self.sale_model.browse(view_data['res_id'])
        self.assertEqual(len(self.sale.order_line), 1)
