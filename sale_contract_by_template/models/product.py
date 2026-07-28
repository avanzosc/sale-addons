# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    contract_tmpl_id = fields.Many2one(
        comodel_name="contract.template",
        string="Contract Template",
        compute="_compute_contract_template",
        inverse="_inverse_contract_template",
        search="_search_contract_template",
    )

    @api.depends_context("company")
    @api.depends("product_variant_ids", "product_variant_ids.contract_tmpl_id")
    def _compute_contract_template(self):
        # Depends on force_company context because contract_tmpl_id is company_dependent
        # on the product_product
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.contract_tmpl_id = template.product_variant_ids.contract_tmpl_id
        for template in self - unique_variants:
            template.contract_tmpl_id = False

    def _inverse_contract_template(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.contract_tmpl_id = (
                    template.contract_tmpl_id
                )

    def _search_contract_template(self, operator, value):
        products = self.env["product.product"].search(
            [("contract_tmpl_id", operator, value)], limit=None
        )
        return [("id", "in", products.mapped("product_tmpl_id").ids)]


class ProductProduct(models.Model):
    _inherit = "product.product"

    contract_tmpl_id = fields.Many2one(
        comodel_name="contract.template",
        string="Contract Template",
        domain="[('contract_type', '=', 'sale')]",
        company_dependent=True,
    )
