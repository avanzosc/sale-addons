# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    catalog_id = fields.Many2one(
        comodel_name="product.catalog",
        string="Catalog",
    )
    catalog_ids = fields.Many2many(
        comodel_name="product.catalog",
        compute="_compute_catalog_ids",
        string="Catalogs",
        store=True,
    )
    is_prebook = fields.Boolean(
        compute="_compute_catalog_ids",
        store=True,
    )

    @api.depends("order_line.catalog_id")
    def _compute_catalog_ids(self):
        for order in self:
            catalogs = order.mapped("order_line.catalog_id")
            order.update(
                {
                    "catalog_ids": catalogs.ids,
                    "is_prebook": any(catalogs.mapped("is_prebook")),
                }
            )

    @api.onchange("catalog_id")
    def _onchange_catalog_id(self):
        for order in self:
            order.order_line.catalog_id = order.catalog_id

    def write(self, vals):
        result = super().write(vals)
        if "catalog_id" in vals:
            self.order_line.write({"catalog_id": vals["catalog_id"]})
        return result
