# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestCatalogDeliveryLead(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Catalog Customer"})
        # Product with its own customer lead time (sale_delay).
        cls.product = cls.env["product.product"].create(
            {"name": "Catalog Test Product", "sale_delay": 5.0}
        )
        Catalog = cls.env["product.catalog"]
        cls.catalog_fast = Catalog.create(
            {"name": "Online catalog", "delivery_lead_days": 2.0}
        )
        cls.catalog_slow = Catalog.create(
            {"name": "Prebook catalog", "delivery_lead_days": 90.0}
        )
        cls.catalog_zero = Catalog.create(
            {"name": "No-lead catalog", "delivery_lead_days": 0.0}
        )

    def _create_order(self, catalog=None):
        vals = {"partner_id": self.partner.id}
        if catalog is not None:
            vals["catalog_id"] = catalog.id
        return self.env["sale.order"].create(vals)

    def _add_line(self, order):
        return self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product.id,
                "product_uom_qty": 1.0,
            }
        )

    def test_no_catalog_keeps_product_lead(self):
        """No catalog on the order -> line keeps the product's lead time."""
        order = self._create_order()
        line = self._add_line(order)
        self.assertFalse(line.catalog_id)
        self.assertEqual(line.customer_lead, 5.0)

    def test_catalog_zero_keeps_product_lead(self):
        """Catalog with 0 delivery days -> line keeps the product's lead time."""
        order = self._create_order(self.catalog_zero)
        line = self._add_line(order)
        self.assertEqual(line.catalog_id, self.catalog_zero)
        self.assertEqual(line.customer_lead, 5.0)

    def test_catalog_positive_overrides_product(self):
        """Catalog with delivery days > 0 -> overrides the product's lead time."""
        order = self._create_order(self.catalog_slow)
        line = self._add_line(order)
        self.assertEqual(line.customer_lead, 90.0)

    def test_change_catalog_updates_existing_lines(self):
        """Changing the order catalog recomputes every line's lead time."""
        order = self._create_order(self.catalog_fast)
        line = self._add_line(order)
        self.assertEqual(line.customer_lead, 2.0)
        order.catalog_id = self.catalog_slow
        self.assertEqual(line.customer_lead, 90.0)

    def test_remove_catalog_reverts_to_product(self):
        """Clearing the catalog reverts lines to the product's lead time."""
        order = self._create_order(self.catalog_slow)
        line = self._add_line(order)
        self.assertEqual(line.customer_lead, 90.0)
        order.catalog_id = False
        self.assertEqual(line.customer_lead, 5.0)

    def test_switch_to_zero_catalog_reverts_to_product(self):
        """Switching to a 0-days catalog reverts lines to the product lead."""
        order = self._create_order(self.catalog_slow)
        line = self._add_line(order)
        self.assertEqual(line.customer_lead, 90.0)
        order.catalog_id = self.catalog_zero
        self.assertEqual(line.customer_lead, 5.0)

    def test_manual_edit_overridden_on_catalog_change(self):
        """A manual lead value is refreshed when the catalog is (re)assigned."""
        order = self._create_order()
        line = self._add_line(order)
        line.customer_lead = 12.0
        self.assertEqual(line.customer_lead, 12.0)
        order.catalog_id = self.catalog_fast
        self.assertEqual(line.customer_lead, 2.0)
