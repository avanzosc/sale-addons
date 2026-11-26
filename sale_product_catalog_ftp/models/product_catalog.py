# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCatalog(models.Model):
    _inherit = "product.catalog"

    upload_ftp_ids = fields.One2many(
        comodel_name="product.catalog.ftp",
        inverse_name="catalog_id",
        readonly=True,
    )
