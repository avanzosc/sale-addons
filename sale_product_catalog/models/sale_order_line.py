# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    catalog_id = fields.Many2one(
        comodel_name="product.catalog",
        string="Catalog",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            order = self.env["sale.order"].browse(vals.get("order_id"))
            if order.catalog_id:
                vals["catalog_id"] = order.catalog_id.id
        return super().create(vals_list)
