# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    catalog_id = fields.Many2one(
        comodel_name="product.catalog",
        compute="_compute_catalog",
        compute_sudo=True,
        store=True,
        readonly=True,
    )

    @api.depends("order_id.catalog_id")
    def _compute_catalog(self):
        for line in self:
            line.catalog_id = line.order_id.catalog_id
