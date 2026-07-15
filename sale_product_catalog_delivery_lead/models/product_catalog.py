# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCatalog(models.Model):
    _inherit = "product.catalog"

    delivery_lead_days = fields.Float(
        string="Delivery Lead Time",
        help="Number of days between the order confirmation and the shipping "
        "of the products. When greater than 0, it overrides the product's "
        "customer lead time on the sale order lines linked to this catalog.",
    )
