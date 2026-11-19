# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleProductAttributeReport(models.TransientModel):
    _name = "open.sale.product.attribute.list.report"
    _description = "Wizard to show Sale Line Product Attributes"

    year_select = fields.Selection(
        selection=[("previous", "Previous"), ("current", "Current"), ("next", "Next")],
        string="Year",
        required=True,
        default="current",
    )
    catalog_id = fields.Many2one(
        string="Catalogue",
        comodel_name="product.catalog.web",
    )
    internal_product_category_id = fields.Many2one(
        string="Internal Product Category",
        comodel_name="internal.product.category",
    )
    product_category_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
    )

    def open_report(self):
        action = self.env.ref(
            "sale_report_product_attributes." "action_product_attribute_sale_report"
        )
        vals = action.read()[0]
        context1 = {
            "year_select": self.year_select,
            "catalog_id": self.catalog_id,
            "internal_product_category_id": self.internal_product_category_id,
            "product_category_id": self.product_category_id,
        }
        vals["context"] = context1
        return vals
