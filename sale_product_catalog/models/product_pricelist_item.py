# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    catalog_ids = fields.Many2many(
        comodel_name="product.catalog",
        relation="pricelist_item_catalog_rel",
        column1="pricelist_item_id",
        column2="catalog_id",
        string="Catalogs",
    )
