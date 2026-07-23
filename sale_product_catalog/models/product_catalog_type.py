# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCatalogType(models.Model):
    _name = "product.catalog.type"
    _description = "Product Catalog Type"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    incompatible_type_ids = fields.Many2many(
        comodel_name="product.catalog.type",
        relation="product_catalog_type_incompatibility_rel",
        column1="catalog_type_id",
        column2="incompatible_type_id",
        string="Incompatible Catalog Types",
    )
