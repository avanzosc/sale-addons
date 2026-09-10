# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    catalog_ids = fields.Many2many(
        comodel_name="product.catalog",
        compute="_compute_catalog_ids",
        string="Catalogs",
        store=True,
    )
    is_prebook = fields.Boolean(
        compute="_compute_catalog_ids",
        string="Prebook",
        store=True,
    )

    @api.depends("order_line.catalog_id")
    def _compute_catalog_ids(self):
        for order in self:
            order.catalog_ids = order.order_line.catalog_id
            order.is_prebook = any(order.catalog_ids.mapped("is_prebook"))
