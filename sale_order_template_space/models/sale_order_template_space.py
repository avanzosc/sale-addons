# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderTemplateSpace(models.Model):
    _name = "sale.order.template.space"
    _description = "Spaces For Sale Order Templates"
    _order = "name"

    name = fields.Char(
        string="Name", required=True, copy=False,
    )
    sale_template_ids = fields.Many2many(
        string="Sale Order Templates", comodel_name="sale.order.template",
        relation="rel_sale_templates_spaces", column1="sale_template_space_id",
        column2="sale_template_id", copy=False,
    )
