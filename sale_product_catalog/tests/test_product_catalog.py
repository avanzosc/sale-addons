# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductCatalog(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "Catalog pricelist"}
        )
        cls.catalog = cls.env["product.catalog"].create({"name": "Catalog"})
        cls.global_catalog = cls.env["product.catalog"].create(
            {"name": "Global catalog"}
        )
        cls.parent_category = cls.env["product.category"].create(
            {"name": "Parent category"}
        )
        cls.child_category = cls.env["product.category"].create(
            {"name": "Child category", "parent_id": cls.parent_category.id}
        )
        cls.other_category = cls.env["product.category"].create(
            {"name": "Other category"}
        )
        cls.variant_product = cls.env["product.product"].create(
            {"name": "Variant product"}
        )
        cls.template_product = cls.env["product.product"].create(
            {"name": "Template product"}
        )
        cls.parent_product = cls.env["product.product"].create(
            {"name": "Parent product", "categ_id": cls.parent_category.id}
        )
        cls.child_product = cls.env["product.product"].create(
            {"name": "Child product", "categ_id": cls.child_category.id}
        )
        cls.other_product = cls.env["product.product"].create(
            {"name": "Other product", "categ_id": cls.other_category.id}
        )
        cls.variant_item = cls._create_item(
            product_id=cls.variant_product.id, catalog=cls.catalog
        )
        cls.template_item = cls._create_item(
            product_tmpl_id=cls.template_product.product_tmpl_id.id,
            catalog=cls.catalog,
        )
        cls.category_item = cls._create_item(
            categ_id=cls.parent_category.id, catalog=cls.catalog
        )
        cls.global_item = cls._create_item(catalog=cls.global_catalog)

    @classmethod
    def _create_item(cls, catalog, **values):
        vals = {
            "pricelist_id": cls.pricelist.id,
            "catalog_ids": [(6, 0, catalog.ids)],
        }
        vals.update(values)
        return cls.env["product.pricelist.item"].create(vals)

    def test_catalog_products_of_each_applied_on(self):
        """The catalog gets the products of every kind of pricelist item."""
        products = self.catalog.product_ids
        self.assertIn(self.variant_product, products)
        self.assertIn(self.template_product, products)
        self.assertIn(self.parent_product, products)
        self.assertIn(self.child_product, products)
        self.assertNotIn(self.other_product, products)

    def test_catalog_products_of_global_item(self):
        """A global pricelist item adds all the products to the catalog."""
        products = self.global_catalog.product_ids
        self.assertEqual(products, self.env["product.product"].search([]))
        self.assertIn(self.other_product, products)

    def test_product_catalogs_of_each_applied_on(self):
        """The products get the catalogs of the items applied to them."""
        self.assertIn(self.catalog, self.variant_product.catalog_ids)
        self.assertIn(self.catalog, self.template_product.catalog_ids)
        self.assertIn(self.catalog, self.parent_product.catalog_ids)
        self.assertIn(self.catalog, self.child_product.catalog_ids)
        self.assertNotIn(self.catalog, self.other_product.catalog_ids)
        self.assertIn(self.global_catalog, self.other_product.catalog_ids)

    def test_remove_catalog_from_item(self):
        """Removing the catalog from an item updates the products."""
        self.variant_item.catalog_ids = [(5, 0, 0)]
        self.assertNotIn(self.catalog, self.variant_product.catalog_ids)
        self.assertNotIn(self.variant_product, self.catalog.product_ids)

    def test_unlink_item(self):
        """Unlinking an item updates the products."""
        self.category_item.unlink()
        self.assertNotIn(self.catalog, self.parent_product.catalog_ids)
        self.assertNotIn(self.catalog, self.child_product.catalog_ids)
        self.assertNotIn(self.parent_product, self.catalog.product_ids)

    def test_change_product_category(self):
        """Moving a product to another category updates its catalogs."""
        self.child_product.categ_id = self.other_category
        self.assertNotIn(self.catalog, self.child_product.catalog_ids)
        self.assertIn(self.catalog, self.parent_product.catalog_ids)

    def test_change_category_parent(self):
        """Moving a category updates the catalogs of its products."""
        self.child_category.parent_id = self.other_category
        self.assertNotIn(self.catalog, self.child_product.catalog_ids)
