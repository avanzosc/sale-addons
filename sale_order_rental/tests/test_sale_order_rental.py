# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from .common import SaleOrderRentalCommon
from odoo.tests import common
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


@common.at_install(False)
@common.post_install(True)
class TestSaleOrderRental(SaleOrderRentalCommon):

    def test_sale_rental_sale_order(self):
        self.assertEquals(self.sale_order.rental_days, 7)
        new_delivery_date = self.delivery_date - relativedelta(days=+1)
        new_end_date = self.end_date + relativedelta(days=+1)
        self.sale_order.write({
            'expected_delivery_date': new_delivery_date,
            'expected_end_date': new_end_date,
        })
        for line in self.sale_order.order_line:
            self.assertNotEquals(
                line.expected_delivery_date, self.delivery_date)
            self.assertEquals(
                line.expected_delivery_date, new_delivery_date)
            self.assertNotEquals(
                line.expected_end_date, self.end_date)
            self.assertEquals(line.expected_end_date, new_end_date)
            with self.assertRaises(ValidationError):
                line.write({
                    'expected_delivery_date': False,
                })
            with self.assertRaises(ValidationError):
                line.write({
                    'expected_delivery_date': self.end_date,
                    'expected_end_date': self.delivery_date,
                })
        self.assertEquals(self.sale_order.rental_days, 9)

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
            lambda p: p.picking_type_code == 'outgoing')
        return_picking = self.sale_order.picking_ids.filtered(
            lambda p: p.picking_type_code == 'incoming')
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
                move.rental_days,
                move.sale_line_id.rental_days)
            with self.assertRaises(ValidationError):
                move.write({
                    'expected_delivery_date':
                        move.sale_line_id.expected_end_date,
                    'expected_end_date':
                        move.sale_line_id.expected_delivery_date,
                })
            with self.assertRaises(ValidationError):
                move.write({
                    'expected_delivery_date': False,
                })
            move.write({
                'expected_delivery_date': (
                    self.delivery_date - relativedelta(days=+1)),
                'expected_end_date': (
                    self.end_date + relativedelta(days=+1)),
            })
            self.assertEquals(
                move.sale_line_id.rental_days, 9)
        out_picking.action_confirm()
        for move in out_picking.move_lines:
            move.move_line_ids.write({
                'qty_done': move.product_uom_qty,
            })
        out_picking._return_rental()  # It won't be able to create return
        out_picking.action_done()
        invoice_ids = self.sale_order.action_invoice_create()
        self.assertEquals(len(invoice_ids), 1)
        for invoice in self.invoice_model.browse(invoice_ids):
            self.assertEquals(self.sale_order.expected_delivery_date,
                              invoice.sale_expected_delivery_date)
            self.assertEquals(self.sale_order.expected_end_date,
                              invoice.sale_expected_end_date)
            self.assertEquals(self.sale_order.rental_days, invoice.rental_days)
        for line in self.sale_order.order_line:
            for invoice_line in line.invoice_lines:
                self.assertEquals(
                    line.expected_delivery_date,
                    invoice_line.sale_expected_delivery_date)
                self.assertEquals(
                    line.expected_end_date,
                    invoice_line.sale_expected_end_date)
                self.assertEquals(
                    line.rental_days, invoice_line.rental_days)
