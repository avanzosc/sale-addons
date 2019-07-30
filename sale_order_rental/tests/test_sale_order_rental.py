# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields
from asn1crypto._ffi import null


class TestSaleOrderRental(TransactionCase):

    def setUp(self):
        super(TestSaleOrderRental, self).setUp()
        self.service_product = self.browse_ref('product.product_delivery_02')
        self.wiz_obj = self.env['sale.advance.payment.inv']
        cond = [('type_tax_use', '=', 'sale'),
                ('amount', '>', 1)]
        self.tax = self.env['account.tax'].search(cond, limit=1)
        cond = [('state', '=', 'draft')]
        self.sale_order = self.env['sale.order'].search(cond, limit=1)
        self.sale_order.write(
            {'expected_delivery_date': '2015-06-09',
             'expected_end_date': '2015-06-15'})
        self.sale_order.order_line.write(
            {'tax_id': [(6, 0, self.tax.ids)]})
        self.sale_order.onchange_expected_end_date()
        self.sale_order.onchange_expected_delivery_date()

    def test_sale_order_rental(self):
        self.sale_order.expected_delivery_date = '2015-06-16'
        with self.assertRaises(ValidationError):
            self.sale_order.onchange_expected_end_date()
            self.sale_order.order_line[0].expected_delivery_date = '2015-06-16'
        self.sale_order.expected_delivery_date = '2015-06-10'
        self.sale_order.onchange_expected_delivery_date()
        for line in self.sale_order.order_line:
            self.assertEquals(line.expected_delivery_date,
                              fields.Date.from_string('2015-06-10'))
            self.assertEquals(line.expected_end_date,
                              fields.Date.from_string('2015-06-15'))
        self.sale_order.order_line[0].product_id_change()
        lines = self.sale_order.mapped('order_line').filtered(
            lambda x: not x.expected_end_date or
            x.expected_end_date != fields.Date.from_string('2015-06-15'))
        self.assertEquals(len(lines), 0)
        lines = self.sale_order.mapped('order_line').filtered(
            lambda x: not x.expected_delivery_date or
            x.expected_delivery_date != fields.Date.from_string('2015-06-10'))
        self.assertEquals(len(lines), 0)
        self.assertEquals(self.sale_order.commitment_date.date(),
                          self.sale_order.expected_delivery_date)
        self.assertEquals(self.sale_order.rental_days, 6)
        self.sale_order.action_confirm()
        self.assertEquals(len(self.sale_order.picking_ids), 2)
        return_picking = self.sale_order.picking_ids[0]
        out_picking = self.sale_order.picking_ids[1]
        self.assertEquals(return_picking.location_id,
                          out_picking.location_dest_id)
        self.assertEquals(return_picking.location_dest_id,
                          out_picking.location_id)
        self.assertEquals(return_picking.picking_type_id,
                          out_picking.picking_type_id.return_picking_type_id)
        self.assertEquals(return_picking.scheduled_date,
                          fields.Datetime.from_string('2015-06-15 08:00:00'))

        for move in return_picking.move_lines:
            self.assertEquals(move.location_id, return_picking.location_id)
            self.assertEquals(move.location_dest_id,
                              return_picking.location_dest_id)
            self.assertEquals(
                move.date_expected,
                fields.Datetime.from_string('2015-06-15 08:00:00'))

        sale_line_vals = {
            'product_id': self.service_product.id,
            'name': self.service_product.name,
            'product_uom_qty': 7,
            'product_uom': self.service_product.uom_id.id,
            'price_unit': self.service_product.list_price}
        self.sale_order.order_line = [(0, 0, sale_line_vals)]

        self.sale_order.action_confirm()
        self.sale_order.expected_delivery_date = 0

        for line in out_picking.move_lines:
            line.quantity_done = line.product_uom_qty

        out_picking.button_validate()
        wiz = self.wiz_obj.with_context(
            active_ids=[self.sale_order.id]).create(
                {'advance_payment_method': 'delivered'})
        wiz.with_context(active_ids=[self.sale_order.id]).create_invoices()
        self.sale_order.write(
            {'expected_delivery_date': False,
             'expected_end_date': False})
        self.sale_order.onchange_expected_end_date()
        self.sale_order.onchange_expected_delivery_date()
        invoice_line = self.sale_order.invoice_ids[0].invoice_line_ids[0]
        for sale in self.sale_order:
            self.assertEquals(sale.expected_delivery_date,
                              False)
            self.assertEquals(sale.expected_end_date,
                              False)

        self.sale_order.expected_delivery_date = '2015-06-05'
        self.sale_order.expected_end_date = '2015-06-10'
        for invoice_line in self.sale_order.invoice_ids:
            self.assertEquals(invoice_line.expected_delivery_date,
                              fields.Date.from_string('2015-06-05'))
            self.assertEquals(invoice_line.expected_end_date,
                              fields.Date.from_string('2015-06-10'))
        for invoice_line in self.sale_order.invoice_ids:
            self.assertEquals(invoice_line.rental_days, 6)
        invoice_line.invoice_line_tax_ids = [(6, 0, self.tax.ids)]
        invoice_line.copy()
        tax = self.sale_order.invoice_ids[0].with_context(
            rental_days=[null]).get_taxes_values()
        for key in tax:
            if 'tax_id' in tax[key]:
                self.assertEquals(tax[key].get('tax_id'), self.tax.id)
        tax_id = 0
        rental_days = 0
        price_unit = 0
        discount = 0.0
        quantity = 0.0
        product_id = 0
        for line in self.sale_order.invoice_ids[0].invoice_line_ids:
            if line.invoice_line_tax_ids:
                tax_id = line.invoice_line_tax_ids[0].id
                rental_days = line.rental_days
                price_unit = line.price_unit
                discount = line.discount
                quantity = line.quantity
                product_id = line.product_id.id
        for line in self.sale_order.invoice_ids[0].invoice_line_ids:
            if not line.invoice_line_tax_ids:
                line.write({
                    'invoice_line_tax_ids': [(6, 0, [tax_id])],
                    'rental_days': rental_days,
                    'price_unit': price_unit,
                    'discount': discount,
                    'quantity': quantity,
                    'product_id': product_id})
        tax = self.sale_order.invoice_ids[0].with_context(
            rental_days=[null]).get_taxes_values()
        for key in tax:
            if 'tax_id' in tax[key]:
                self.assertEquals(tax[key].get('tax_id'), self.tax.id)
