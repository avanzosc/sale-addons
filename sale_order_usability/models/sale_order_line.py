# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_order = fields.Datetime(
        related="order_id.date_order", store=True, readonly=True, index=True, copy=False
    )
    partner_invoice_id = fields.Many2one(
        related="order_id.partner_invoice_id", store=True, readonly=True, index=True
    )
