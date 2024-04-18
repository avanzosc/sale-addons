# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_categ_id = fields.Many2one(
        string="Product Category", comodel_name="product.category",
        related="product_id.categ_id", store=True, copy=False,
    )
    section_line_id = fields.Many2one(
        string="Section line", comodel_name="sale.order.line", copy=False,
    )
