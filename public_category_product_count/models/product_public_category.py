# Copyright 2025 Eñaut Alberdi Korta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    product_count = fields.Integer(
        string="Number of Products",
        compute="_compute_product_count",
        store=False,
        compute_sudo=True,
    )

    @api.depends_context("website_id")
    def _compute_product_count(self):
        Product = self.env["product.template"]

        if not self:
            return

        category_ids = self.ids

        data = Product.read_group(
            domain=[("public_categ_ids", "in", category_ids)],
            fields=["public_categ_ids"],
            groupby=["public_categ_ids"],
        )

        count_dict = {
            entry["public_categ_ids"][0]: entry["public_categ_ids_count"]
            for entry in data
            if entry.get("public_categ_ids")
        }

        for category in self:
            category.product_count = count_dict.get(category.id, 0)

    def action_open_category_products(self):
        self.ensure_one()

        product_action = self.env.ref(
            "product.product_template_action", raise_if_not_found=False
        )

        action_vals = {
            "type": "ir.actions.act_window",
            "name": f"Products in {self.display_name}",
            "res_model": "product.template",
            "view_mode": "tree,form",
            "target": "current",
            "domain": [("public_categ_ids", "in", [self.id])],
            "context": {"default_public_categ_ids": [self.id]},
        }

        if product_action:
            base = product_action.read()[0]
            action_vals.update(
                {k: base[k] for k in base if k not in ["domain", "context"]}
            )

        action_vals["domain"] = [("public_categ_ids", "in", [self.id])]
        return action_vals

    def action_recalculate_product_count(self):
        for record in self:
            record._compute_product_count()
        return True
