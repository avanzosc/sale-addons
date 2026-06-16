# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ProductCatalog(models.Model):
    _name = "product.catalog"
    _description = "Product Catalog"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    logo = fields.Binary()
    description = fields.Text(translate=True)
    inventory_availability = fields.Selection(
        selection=[
            ("never", "Never"),
            ("always", "Always"),
            ("threshold", "On Threshold"),
            ("custom", "Custom"),
        ],
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        required=True,
        default=lambda self: self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        ),
    )
    pricelist_item_ids = fields.Many2many(
        comodel_name="product.pricelist.item",
        relation="pricelist_item_catalog_rel",
        column1="catalog_id",
        column2="pricelist_item_id",
        string="Pricelist Items",
    )
    pricelist_item_count = fields.Integer(
        compute="_compute_pricelist_item_count",
        compute_sudo=True,
    )

    def _compute_pricelist_item_count(self):
        for rec in self:
            rec.pricelist_item_count = len(rec.pricelist_item_ids)

    def action_pricelist_items(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Pricelist Items"),
            "res_model": "product.pricelist.item",
            "view_mode": "list,pivot,form",
            "domain": [("catalog_ids", "in", self.ids)],
            "context": {"search_default_fixed_price": 1},
        }
