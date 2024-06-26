# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_order_space_id = fields.Many2one(
        string="Sale Order Space",
        comodel_name="sale.order.space",
        copy=False,
    )
