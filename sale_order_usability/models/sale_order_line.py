# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        related="order_id.date_order", store=True, readonly=True, index=True, copy=False
    )
    product_default_code = fields.Char(
        string="Product Internal Reference", related="product_id.default_code",
        store=True, readonly=True, index=True, copy=False
    )
