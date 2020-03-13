# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderTemplateOption(models.Model):
    _inherit = "sale.order.template.option"

    company_id = fields.Many2one(
        string="Company", comodel_name="res.company",
        related="product_id.company_id", store=True)
    school_id = fields.Many2one(
        string="Education Center", comodel_name="res.partner",
        related="sale_order_template_id.school_id")
