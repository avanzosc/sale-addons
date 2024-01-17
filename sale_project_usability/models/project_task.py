# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    sale_line_product_id = fields.Many2one(
        string="Sale line product",
        comodel_name="product.product",
        related="sale_line_id.product_id",
        store=True,
    )
    sale_line_product_uom_qty = fields.Float(
        string="Sale line quantity",
        digits="Product Unit of Measure",
        related="sale_line_id.product_uom_qty",
        store=True,
    )
