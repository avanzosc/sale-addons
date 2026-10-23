# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


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
    )

    @api.depends(
        "catalog_pricelist_item_ids.catalog_ids",
        "catalog_pricelist_item_ids.applied_on",
        "categ_id",
        "categ_id.parent_path",
        "product_tmpl_id",
    )
    def _compute_catalog_ids(self):
        today = fields.Date.today()
        item_model = self.env["product.pricelist.item"]
        for product in self:
            items = item_model.search(
                [
                    "|",
                    "|",
                    "|",
                    "&",
                    ("applied_on", "=", "0_product_variant"),
                    ("product_id", "=", product.id),
                    "&",
                    ("applied_on", "=", "1_product"),
                    ("product_tmpl_id", "=", product.product_tmpl_id.id),
                    "&",
                    ("applied_on", "=", "2_product_category"),
                    ("categ_id", "parent_of", product.categ_id.id),
                    ("applied_on", "=", "3_global"),
                ]
            )
            product.catalog_ids = items.filtered(
                lambda pi: (
                    (not pi.date_start or pi.date_start.date() <= today)
                    and (not pi.date_end or pi.date_end.date() >= today)
                )
            ).mapped("catalog_ids")
