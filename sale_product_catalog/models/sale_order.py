# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    catalog_id = fields.Many2one(
        comodel_name="product.catalog",
        string="Catalog",
    )

    @api.onchange("catalog_id")
    def _onchange_catalog_id(self):
        for order in self:
            if order.catalog_id.warehouse_id:
                order.warehouse_id = order.catalog_id.warehouse_id
