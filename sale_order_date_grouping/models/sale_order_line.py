# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sale_month = fields.Char(
        related="order_id.sale_month",
        store=True,
        string="Sale Month",
    )
    sale_year = fields.Char(
        related="order_id.sale_year",
        store=True,
        string="Sale Year",
    )
    sale_quarter = fields.Char(
        related="order_id.sale_quarter",
        store=True,
        string="Sale Quarter",
    )
