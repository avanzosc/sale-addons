# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

APPLIED_ON_VARIANT = "0_product_variant"
APPLIED_ON_PRODUCT = "1_product"
APPLIED_ON_CATEGORY = "2_product_category"
APPLIED_ON_GLOBAL = "3_global"


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    catalog_ids = fields.Many2many(
        comodel_name="product.catalog",
        relation="pricelist_item_catalog_rel",
        column1="pricelist_item_id",
        column2="catalog_id",
        string="Catalogs",
    )

    def _get_applicable_products(self):
        """Return the products affected by these pricelist items.

        The products depend on the 'applied_on' option of every item:
        '0_product_variant' for the variant set in the item, '1_product' for
        all the variants of the product template, '2_product_category' for all
        the products of the category (including the ones of its child
        categories) and '3_global' for all the products.
        """
        products = self.env["product.product"].browse()
        variant_items = self.filtered(lambda x: x.applied_on == APPLIED_ON_VARIANT)
        products |= variant_items.mapped("product_id")
        template_items = self.filtered(lambda x: x.applied_on == APPLIED_ON_PRODUCT)
        if template_items:
            products |= self.env["product.product"].search(
                [
                    (
                        "product_tmpl_id",
                        "in",
                        template_items.mapped("product_tmpl_id").ids,
                    )
                ]
            )
        category_items = self.filtered(lambda x: x.applied_on == APPLIED_ON_CATEGORY)
        if category_items:
            categories = self.env["product.category"].search(
                [("id", "child_of", category_items.mapped("categ_id").ids)]
            )
            products |= self.env["product.product"].search(
                [("categ_id", "in", categories.ids)]
            )
        if self.filtered(lambda x: x.applied_on == APPLIED_ON_GLOBAL):
            products |= self.env["product.product"].search([])
        return products

    def _get_affected_products(self):
        """Return the products whose catalogs depend on these items.

        Only the items belonging to a catalog have any effect on the catalogs
        of the products.
        """
        products = self.env["product.product"].browse()
        for item in self:
            if not item.catalog_ids:
                continue
            if item.applied_on == APPLIED_ON_VARIANT:
                products |= item.product_id
            elif item.applied_on == APPLIED_ON_PRODUCT:
                products |= self.env["product.product"].search(
                    [("product_tmpl_id", "=", item.product_tmpl_id.id)]
                )
            elif item.applied_on == APPLIED_ON_CATEGORY:
                categories = self.env["product.category"].search(
                    [("id", "child_of", item.categ_id.ids)]
                )
                products |= self.env["product.product"].search(
                    [("categ_id", "in", categories.ids)]
                )
            else:
                products |= self.env["product.product"].search([])
        return products
