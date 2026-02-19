# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestSaleLinePendingInfo(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_model = cls.env["sale.order"]
        cls.report_model = cls.env["sale.report"]

        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "product",
                "list_price": 100.0,
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 10,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )

    def test_sale_line_pending_info(self):
        sale = self.sale_order
        sale.order_line.write({"discount": 10})
        sale.action_confirm()

        for line in sale.order_line:
            if line.qty_delivered_method == "stock_move":
                self.assertEqual(
                    line.qty_pending_delivery, line.product_uom_qty - line.qty_delivered
                )
            else:
                self.assertEqual(line.qty_pending_delivery, 0)

            amount = line.qty_pending_delivery * line.price_unit
            if line.discount:
                amount *= 1 - (line.discount or 0.0) / 100.0
            self.assertAlmostEqual(
                line.amount_pending_delivery,
                amount,
                places=2,
                msg="Amount pending delivery calculation error",
            )

            self.assertEqual(
                line.qty_pending_invoicing, line.product_uom_qty - line.qty_invoiced
            )

            amount = line.qty_pending_invoicing * line.price_unit
            if line.discount:
                amount *= 1 - (line.discount or 0.0) / 100.0
            self.assertAlmostEqual(
                line.amount_pending_invoicing,
                amount,
                places=2,
                msg="Amount pending invoicing calculation error",
            )

            expected_shipped_pending = max(line.qty_delivered - line.qty_invoiced, 0.0)
            self.assertEqual(
                line.qty_shipped_pending_invoicing,
                expected_shipped_pending,
                msg="Shipped pending invoicing quantity error",
            )

            amount = line.qty_shipped_pending_invoicing * line.price_unit
            if line.discount:
                amount *= 1 - (line.discount or 0.0) / 100.0
            self.assertAlmostEqual(
                line.amount_shipped_pending_invoicing,
                amount,
                places=2,
                msg="Amount shipped pending invoicing calculation error",
            )

        self.assertEqual(
            sale.total_qty_pending_delivery,
            sum(sale.order_line.mapped("qty_pending_delivery")),
            msg="Total qty pending delivery mismatch",
        )

        self.assertAlmostEqual(
            sale.total_amount_pending_delivery,
            sum(sale.order_line.mapped("amount_pending_delivery")),
            places=2,
            msg="Total amount pending delivery mismatch",
        )

        self.assertEqual(
            sale.total_qty_pending_invoicing,
            sum(sale.order_line.mapped("qty_pending_invoicing")),
            msg="Total qty pending invoicing mismatch",
        )

        self.assertAlmostEqual(
            sale.total_amount_pending_invoicing,
            sum(sale.order_line.mapped("amount_pending_invoicing")),
            places=2,
            msg="Total amount pending invoicing mismatch",
        )

        self.assertEqual(
            sale.total_qty_shipped_pending_invoicing,
            sum(sale.order_line.mapped("qty_shipped_pending_invoicing")),
            msg="Total qty shipped pending invoicing mismatch",
        )

        self.assertAlmostEqual(
            sale.total_amount_shipped_pending_invoicing,
            sum(sale.order_line.mapped("amount_shipped_pending_invoicing")),
            places=2,
            msg="Total amount shipped pending invoicing mismatch",
        )

        res = self.report_model._query()
        self.assertIn(
            "qty_pending_delivery",
            str(res),
            msg="qty_pending_delivery not found in sale report",
        )
        self.assertIn(
            "qty_pending_invoicing",
            str(res),
            msg="qty_pending_invoicing not found in sale report",
        )
        self.assertIn(
            "amount_pending_delivery",
            str(res),
            msg="amount_pending_delivery not found in sale report",
        )
        self.assertIn(
            "amount_pending_invoicing",
            str(res),
            msg="amount_pending_invoicing not found in sale report",
        )

    def test_sale_order_totals(self):
        """
        Test adicional para verificar los cálculos de totales ordenados
        y entregados
        """
        sale = self.sale_order
        sale.action_confirm()

        self.assertEqual(
            sale.qty_ordered,
            sum(
                line.product_uom_qty
                for line in sale.order_line
                if line.state != "cancel"
            ),
            msg="Total ordered quantity mismatch",
        )

        self.assertEqual(
            sale.qty_delivered,
            sum(
                line.qty_delivered for line in sale.order_line if line.state != "cancel"
            ),
            msg="Total delivered quantity mismatch",
        )

    def test_cancelled_lines_excluded(self):
        """
        Test que verifica que las líneas canceladas no se incluyen
        en los totales
        """
        sale = self.sale_order
        sale.action_confirm()

        line_to_cancel = sale.order_line[0]
        line_to_cancel.write({"product_uom_qty": 0})

        self.assertEqual(
            sale.qty_ordered,
            sum(
                line.product_uom_qty
                for line in sale.order_line
                if line.state != "cancel"
            ),
            msg="Cancelled lines should be excluded from ordered total",
        )

