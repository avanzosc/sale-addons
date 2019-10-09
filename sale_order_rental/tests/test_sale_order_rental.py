# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderRental(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderRental, cls).setUpClass()
        cls.service_product = cls.env.ref('product.product_delivery_02')
        cond = [('type_tax_use', '=', 'sale'),
                ('amount', '>', 1)]
        cls.tax = cls.env['account.tax'].search(cond, limit=1)
        cond = [('state', '=', 'draft')]
        cls.sale_order = cls.env['sale.order'].search(cond, limit=1)
        cls.sale_order.order_line.write({
            'expected_delivery_date': '2015-06-09',
            'expected_end_date': '2015-06-15',
            'tax_id': [(6, 0, cls.tax.ids)],
        })

    def test_sale_order_rental(self):
        for line in self.sale_order.order_line:
            self.assertEquals(line.expected_delivery_date,
                              self.sale_order.expected_delivery_date)
            self.assertEquals(line.expected_end_date,
                              self.sale_order.expected_end_date)
        self.sale_order._onchange_expected_delivery_date()
        self.assertEquals(self.sale_order.commitment_date.date(),
                          self.sale_order.expected_delivery_date)
        self.assertEquals(self.sale_order.rental_days, 7)
        self.sale_order.action_confirm()
        self.assertEquals(len(self.sale_order.picking_ids), 2)
        out_picking = self.sale_order.picking_ids.filtered(
            lambda p: p.picking_type_code == 'customer')
        return_picking = self.sale_order.picking_ids.filtered(
            lambda p: p.picking_type_code == 'supplier')
        self.assertEquals(
            out_picking.location_id, return_picking.location_dest_id)
        self.assertEquals(
            out_picking.picking_type_id,
            return_picking.picking_type_id.return_picking_type_id)
        for move in out_picking.move_lines:
            self.assertEquals(
                move.expected_delivery_date,
                move.sale_line_id.expected_delivery_date)
            self.assertEquals(
                move.expected_end_date,
                move.sale_line_id.expected_end_date)
            self.assertEquals(
                move.expected_delivery_date,
                move.sale_line_id.rental_days)
        # for line in out_picking.move_lines:
        #     line.quantity_done = line.product_uom_qty
        #
        # out_picking.button_validate()
        # wiz = self.wiz_obj.with_context(
        #     active_ids=[self.sale_order.id]).create(
        #         {'advance_payment_method': 'delivered'})
        # wiz.with_context(active_ids=[self.sale_order.id]).create_invoices()
        # self.sale_order.write(
        #     {'expected_delivery_date': False,
        #      'expected_end_date': False})
        # self.sale_order.onchange_expected_end_date()
        # self.sale_order.onchange_expected_delivery_date()
        # invoice_line = self.sale_order.invoice_ids[0].invoice_line_ids[0]
        # for sale in self.sale_order:
        #     self.assertEquals(sale.expected_delivery_date,
        #                       False)
        #     self.assertEquals(sale.expected_end_date,
        #                       False)
        #
        # self.sale_order.expected_delivery_date = '2015-06-05'
        # self.sale_order.expected_end_date = '2015-06-10'
        # for invoice_line in self.sale_order.invoice_ids:
        #     self.assertEquals(invoice_line.expected_delivery_date,
        #                       fields.Date.from_string('2015-06-05'))
        #     self.assertEquals(invoice_line.expected_end_date,
        #                       fields.Date.from_string('2015-06-10'))
        # for invoice_line in self.sale_order.invoice_ids:
        #     self.assertEquals(invoice_line.rental_days, 6)
        # invoice_line.invoice_line_tax_ids = [(6, 0, self.tax.ids)]
        # invoice_line.copy()
        # tax = self.sale_order.invoice_ids[0].with_context(
        #     rental_days=[]).get_taxes_values()
        # for key in tax:
        #     if 'tax_id' in tax[key]:
        #         self.assertEquals(tax[key].get('tax_id'), self.tax.id)
        # tax_id = 0
        # rental_days = 0
        # price_unit = 0
        # discount = 0.0
        # quantity = 0.0
        # product_id = 0
        # for line in self.sale_order.invoice_ids[0].invoice_line_ids:
        #     if line.invoice_line_tax_ids:
        #         tax_id = line.invoice_line_tax_ids[0].id
        #         rental_days = line.rental_days
        #         price_unit = line.price_unit
        #         discount = line.discount
        #         quantity = line.quantity
        #         product_id = line.product_id.id
        # for line in self.sale_order.invoice_ids[0].invoice_line_ids:
        #     if not line.invoice_line_tax_ids:
        #         line.write({
        #             'invoice_line_tax_ids': [(6, 0, [tax_id])],
        #             'rental_days': rental_days,
        #             'price_unit': price_unit,
        #             'discount': discount,
        #             'quantity': quantity,
        #             'product_id': product_id})
        # tax = self.sale_order.invoice_ids[0].with_context(
        #     rental_days=[]).get_taxes_values()
        # for key in tax:
        #     if 'tax_id' in tax[key]:
        #         self.assertEquals(tax[key].get('tax_id'), self.tax.id)
