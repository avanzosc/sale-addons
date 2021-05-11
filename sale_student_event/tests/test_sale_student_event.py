# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestSaleStudentEvent(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleStudentEvent, cls).setUpClass()
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product1 = cls.env['product.product'].create({
            'name': 'Product 1 sale student event',
            'type': 'service',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.product2 = cls.env['product.product'].create({
            'name': 'Product 2 sale student event',
            'type': 'service',
            'default_code': 'P2',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.product3 = cls.env['product.product'].create({
            'name': 'Product 3 sale student event',
            'type': 'service',
            'default_code': 'P3',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.event = cls.env.ref('event.event_1')
        cls.ticket = cls.env['event.event.ticket'].create({
            'event_id': cls.event.id,
            'name': cls.product1.name,
            'product_id': cls.product1.id,
            'is_member': True,
            'price': 8.00,
            'seats_max': 0,
            'seats_reserved': 0,
            'seats_unconfirmed': 0
            })
        cls.ticket = cls.env['event.event.ticket'].create({
            'event_id': cls.event.id,
            'name': cls.product2.name,
            'product_id': cls.product2.id,
            'is_member': False,
            'price': 10.00,
            'seats_max': 0,
            'seats_reserved': 0,
            'seats_unconfirmed': 0
            })
        cls.sale_model = cls.env['sale.order']
        cls.partner1 = cls.env['res.partner'].create({
            'name': 'Partner1 sale student event',
        })
        cls.partner2 = cls.env['res.partner'].create({
            'name': 'Partner2 sale student event',
            'parent_id': cls.partner1.id,
            })
        cls.sale_order = cls.sale_model.create({
            'partner_id': cls.partner1.id,
            'client_order_ref': 'New reference',
            'order_line': [(0, 0, {'product_id': cls.product1.id,
                                   'name': cls.product1.name,
                                   'is_member': True,
                                   'event_id': cls.event.id})],
            })

    def test_sale_student_event(self):
        line = self.sale_order.order_line[0]
        line._onchange_event_is_member()
        self.assertEqual(line.product_id, self.product1)
        self.assertEqual(line.price_unit, 8.0)
