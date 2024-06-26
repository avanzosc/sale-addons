# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    space_ids = fields.Many2many(
        string="Spaces",
        comodel_name="sale.order.template.space",
        copy=False,
    )
    product_categ_id = fields.Many2one(
        string="Product Category",
        comodel_name="product.category",
        related="product_id.categ_id",
        store=True,
        copy=False,
    )
    sequence_to_view = fields.Integer(
        string="Sequence",
        compute="_compute_sequence_to_view",
        store=True,
        copy=False,
    )

    @api.depends("sequence")
    def _compute_sequence_to_view(self):
        for line in self:
            line.sequence_to_view = line.sequence
