# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestSaleStockMoveCost(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test SMC Partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test SMC Product",
                "type": "consu",
                "list_price": 100.0,
                "standard_price": 0.0,
            }
        )

    def _create_confirmed_order(self, qty, price_unit):
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": qty,
                            "price_unit": price_unit,
                        },
                    )
                ],
            }
        )
        order.action_confirm()
        return order

    def _add_move_with_cost(self, line, qty, price_unit_cost):
        """Create one extra stock.move on the sale line with a costed move line."""
        base_move = line.move_ids[:1]
        move = base_move.copy(
            {
                "sale_line_id": line.id,
                "product_uom_qty": 0,
                "move_line_ids": False,
            }
        )
        self.env["stock.move.line"].create(
            {
                "move_id": move.id,
                "picking_id": move.picking_id.id,
                "product_id": self.product.id,
                "product_uom_id": self.product.uom_id.id,
                "location_id": move.location_id.id,
                "location_dest_id": move.location_dest_id.id,
                "quantity": qty,
                "price_unit_cost": price_unit_cost,
            }
        )
        return move

    def test_order_cost_not_double_counted_on_multiple_moves(self):
        """A line with several moves must not accumulate cost triangularly.

        Regression test for the bug where ``sale_order_cost`` was summed
        inside the moves loop using the running ``sale_line_cost`` total,
        so two moves of 7.50 produced 22.50 instead of 15.00.
        """
        order = self._create_confirmed_order(qty=2, price_unit=100.0)
        line = order.order_line
        # Clear any reservation move line so only our costed lines count.
        line.move_ids.move_line_ids.unlink()
        # Two costed moves of 7.50 each on the same sale line.
        self._add_move_with_cost(line, qty=1, price_unit_cost=7.5)
        self._add_move_with_cost(line, qty=1, price_unit_cost=7.5)
        order.invalidate_recordset()

        self.assertEqual(line.sale_line_cost, 15.0)
        # The header total must equal the sum of the line costs (the invariant
        # the bug broke). It must be 15.00, never 22.50.
        self.assertEqual(order.sale_order_cost, 15.0)
        self.assertEqual(
            order.sale_order_cost, sum(order.order_line.mapped("sale_line_cost"))
        )
        # Margin = subtotal - cost, consistent at line and order level.
        self.assertEqual(line.sale_line_margin, line.price_subtotal - 15.0)
        self.assertEqual(order.sale_order_margin, line.price_subtotal - 15.0)

    def test_cancelled_moves_are_ignored(self):
        """Cancelled moves must not contribute to the cost."""
        order = self._create_confirmed_order(qty=2, price_unit=100.0)
        line = order.order_line
        line.move_ids.move_line_ids.unlink()
        self._add_move_with_cost(line, qty=1, price_unit_cost=7.5)
        cancel_move = self._add_move_with_cost(line, qty=1, price_unit_cost=7.5)
        cancel_move._action_cancel()
        order.invalidate_recordset()

        self.assertEqual(line.sale_line_cost, 7.5)
        self.assertEqual(order.sale_order_cost, 7.5)
