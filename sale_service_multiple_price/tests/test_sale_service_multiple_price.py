# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import SaleServiceMultiplePrice
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestSaleServiceMultiplePrice(SaleServiceMultiplePrice):

    def test_sale_service_multiple_price(self):
        self.assertTrue(self.sale_order.timesheet_ids)
        self.sale_order._create_invoices()
        for so_line in self.sale_order.order_line:
            self.assertEquals(len(so_line.invoice_lines), 2)
            self.assertEquals(
                so_line.qty_delivered,
                sum(so_line.mapped("invoice_lines.quantity")))
            self.assertEquals(
                so_line.invoice_lines[:1].quantity, self.timesheet_count)
            self.assertEquals(
                so_line.invoice_lines[:1].price_unit, so_line.price_unit)
            self.assertEquals(
                so_line.invoice_lines[1:].quantity,
                so_line.qty_delivered - self.timesheet_count)
            self.assertEquals(
                so_line.invoice_lines[1:].price_unit,
                so_line.multiple_price_unit)

