# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.exceptions import ValidationError, UserError


class TestSaleFromPicking(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleFromPicking, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.sale_model = cls.env['sale.order']
        cls.picking_model = cls.env['stock.picking']
        cls.generate_wiz = cls.env['generate.sale.orders.wizard']
        cls.trasnf_obj = cls.env['stock.immediate.transfer']
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.p_partner = cls.partner_model.create({
            'name': 'Partner2',
        })
        cls.supplier_location = cls.env.ref(
            'stock.stock_location_suppliers').id
        cls.product_1 = cls.product_model.create({
            'name': 'Product_1',
            'type': 'product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.product_2 = cls.product_model.create({
            'name': 'Product_2',
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
            'name': self.product_1.name,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'product_uom': self.product_1.uom_id.id,
            'picking_id': self.picking1.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id})
        with self.assertRaises(UserError):
            # No partner
            self.picking1.create_sale_order()
        self.picking1.partner_id = self.partner.id
        view_data = self.picking1.create_sale_order()
        self.sale = self.sale_model.browse(view_data['res_id'])
        self.assertEqual(len(self.sale.order_line), 1)

    def test_generate_multiple_sales(self):
        picking_values_1 = {
            'picking_type_id': self.warehouse1.in_type_id.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id,
            'partner_id': self.partner.id,
            'name': 'Pick_1'
        }
        self.picking_1 = self.picking_model.create(picking_values_1)
        self.env['stock.move'].create({
            'name': self.product_1.name,
            'product_id': self.product_1.id,
            'product_uom_qty': 1,
            'product_uom': self.product_1.uom_id.id,
            'picking_id': self.picking_1.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id,
            })
        picking_values_2 = {
            'picking_type_id': self.warehouse1.in_type_id.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id,
            'partner_id': self.partner.id,
            'name': 'Pick_2'
        }
        self.picking_2 = self.picking_model.create(picking_values_2)
        self.env['stock.move'].create({
            'name': self.product_2.name,
            'product_id': self.product_2.id,
            'product_uom_qty': 1,
            'product_uom': self.product_2.uom_id.id,
            'picking_id': self.picking_2.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id})
        self.trasnf_obj.create(
            {'pick_ids': [(4, self.picking_1.id)]}).process()
        self.trasnf_obj.create(
            {'pick_ids': [(4, self.picking_2.id)]}).process()
        self.env['stock.quant']._update_available_quantity(
            self.product_1, self.env.ref('stock.stock_location_stock'), 2)
        self.env['stock.quant']._update_available_quantity(
            self.product_2, self.env.ref('stock.stock_location_stock'), 2)
        self.generate_pick_wiz_model = self.generate_wiz.with_context(
            active_model=self.picking_model._name,
            active_ids=[self.picking_1.id,
                        self.picking_2.id]).generate_sale_orders()
        self.assertEqual(self.picking_1.sale_order_id.state, 'sale')
        self.assertEqual(self.picking_2.sale_order_id.picking_ids[0].state,
                         'done')
        with self.assertRaises(ValidationError):
            self.generate_pick_wiz_model = self.generate_wiz.with_context(
                active_model=self.picking_model._name,
                active_ids=[self.picking_1.id]).generate_sale_orders()
        picking_values_3 = {
            'picking_type_id': self.warehouse1.out_type_id.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.warehouse1.lot_stock_id.id,
            'partner_id': self.partner.id,
            'name': 'Pick_3'
        }
        self.picking_3 = self.picking_model.create(picking_values_3)
        with self.assertRaises(ValidationError):
            self.generate_pick_wiz_model = self.generate_wiz.with_context(
                active_model=self.picking_model._name,
                active_ids=[self.picking_3.id]).generate_sale_orders()
