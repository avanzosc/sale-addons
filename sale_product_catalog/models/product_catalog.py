# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class ProductCatalog(models.Model):
    _name = "product.catalog"
    _description = "Product Catalog"
    _order = "sequence, name"

    def _get_default_catalog_type_id(self):
        return self.env["product.catalog.type"].search([], limit=1)

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(required=True, default=10)
    active = fields.Boolean(default=True)
    logo = fields.Binary()
    description = fields.Text(translate=True)
    catalog_type_id = fields.Many2one(
        comodel_name="product.catalog.type",
        string="Catalog Type",
        ondelete="restrict",
        default=_get_default_catalog_type_id,
        required=True,
    )
    is_prebook = fields.Boolean(
        related="catalog_type_id.is_prebook",
    )
    date_start = fields.Date(string="Sale Start Date")
    date_end = fields.Date(string="Sale End Date")
    commitment_date = fields.Date()
    inventory_availability = fields.Selection(
        selection=[
            ("never", "Never"),
            ("always", "Always"),
            ("threshold", "On Threshold"),
            ("custom", "Custom"),
        ],
        default="never",
        required=True,
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
        domain=[
            "&",
            "|",
            ("product_tmpl_id", "=", False),
            ("product_tmpl_id.active", "=", True),
            "|",
            ("product_id", "=", False),
            ("product_id.active", "=", True),
        ],
    )
    pricelist_item_count = fields.Integer(
        compute="_compute_pricelist_item_count",
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        compute="_compute_products",
    )
    product_count = fields.Integer(
        compute="_compute_products",
    )
    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        compute="_compute_products",
    )
    product_tmpl_count = fields.Integer(
        compute="_compute_products",
    )
    pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        compute="_compute_pricelist_ids",
    )

    def _compute_pricelist_item_count(self):
        for rec in self:
            rec.pricelist_item_count = len(rec.pricelist_item_ids)

    def _compute_products(self):
        today = fields.Date.today()
        template_model = self.env["product.template"]
        variant_model = self.env["product.product"]
        for rec in self:
            price_items = rec.pricelist_item_ids.filtered(
                lambda pi: (
                    (not pi.date_start or pi.date_start.date() <= today)
                    and (not pi.date_end or pi.date_end.date() >= today)
                )
            )
            templates = template_model
            products = variant_model
            for item in price_items:
                if item.applied_on == "0_product_variant":
                    products |= item.product_id
                    templates |= item.product_id.product_tmpl_id
                elif item.applied_on == "1_product":
                    templates |= item.product_tmpl_id
                elif item.applied_on == "2_product_category":
                    templates |= template_model.search(
                        [("categ_id", "child_of", item.categ_id.id)]
                    )
                elif item.applied_on == "3_global":
                    templates |= template_model.search([])
            templates = templates.filtered(lambda p: p.active)
            products = products.filtered(lambda p: p.active)
            rec.update(
                {
                    "product_ids": [(6, 0, products.ids)],
                    "product_tmpl_ids": [(6, 0, templates.ids)],
                    "product_count": len(products),
                    "product_tmpl_count": len(templates),
                }
            )

    def _compute_pricelist_ids(self):
        for rec in self:
            rec.pricelist_ids = [
                (6, 0, rec.mapped("pricelist_item_ids.pricelist_id").ids)
            ]

    def action_open_pricelist_items(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product.product_pricelist_item_action"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.pricelist_item_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

    def action_open_product_templates(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product.product_template_action_all"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.product_tmpl_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action

    def action_open_product_variants(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product.product_normal_action"
        )
        action["domain"] = expression.AND(
            [
                [("id", "in", self.product_ids.ids)],
                safe_eval(action.get("domain") or "[]"),
            ]
        )
        return action
