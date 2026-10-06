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
        store=True,
    )

    @api.depends("catalog_pricelist_item_ids.catalog_ids")
    def _compute_catalog_ids(self):
        for product in self:
            product.catalog_ids = product.catalog_pricelist_item_ids.catalog_ids
