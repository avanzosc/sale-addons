# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import defaultdict

from odoo import api, fields, models

from .product_pricelist_item import (
    APPLIED_ON_CATEGORY,
    APPLIED_ON_GLOBAL,
    APPLIED_ON_PRODUCT,
)


class ProductProduct(models.Model):
    _inherit = "product.product"

    catalog_pricelist_item_ids = fields.One2many(
        comodel_name="product.pricelist.item",
        inverse_name="product_id",
    )
    catalog_ids = fields.Many2many(
        comodel_name="product.catalog",
        string="Catalogs",
        compute="_compute_catalog_ids",
        store=True,
    )

    @api.depends("catalog_pricelist_item_ids.catalog_ids")
    def _compute_catalog_ids(self):
        items = self.env["product.pricelist.item"]
        empty_catalogs = self.env["product.catalog"].browse()
        # Items applied on the variant itself
        catalogs_by_variant = defaultdict(lambda: empty_catalogs)
        for item in self.mapped("catalog_pricelist_item_ids"):
            catalogs_by_variant[item.product_id.id] |= item.catalog_ids
        # Items applied on the product template
        catalogs_by_template = defaultdict(lambda: empty_catalogs)
        template_items = items.search(
            [
                ("applied_on", "=", APPLIED_ON_PRODUCT),
                ("product_tmpl_id", "in", self.mapped("product_tmpl_id").ids),
            ]
        )
        for item in template_items:
            catalogs_by_template[item.product_tmpl_id.id] |= item.catalog_ids
        # Items applied on the product category or on any of its parent
        # categories
        catalogs_by_category = defaultdict(lambda: empty_catalogs)
        parent_categories = self.env["product.category"].search(
            [("id", "parent_of", self.mapped("categ_id").ids)]
        )
        category_items = items.search(
            [
                ("applied_on", "=", APPLIED_ON_CATEGORY),
                ("categ_id", "in", parent_categories.ids),
            ]
        )
        for item in category_items:
            catalogs_by_category[item.categ_id.id] |= item.catalog_ids
        # Items applied on all the products
        global_catalogs = items.search(
            [("applied_on", "=", APPLIED_ON_GLOBAL)]
        ).catalog_ids
        for product in self:
            catalogs = catalogs_by_variant[product.id]
            catalogs |= catalogs_by_template[product.product_tmpl_id.id]
            for category_id in self._get_category_ancestor_ids(product.categ_id):
                catalogs |= catalogs_by_category[category_id]
            catalogs |= global_catalogs
            product.catalog_ids = catalogs

    def _get_category_ancestor_ids(self, category):
        """Return the ids of the category and of all its parent categories."""
        return [int(x) for x in (category.parent_path or "").split("/") if x]

    def _update_catalog_ids(self):
        """Mark the catalogs of the products to be recomputed."""
        self.env.add_to_compute(self._fields["catalog_ids"], self)
