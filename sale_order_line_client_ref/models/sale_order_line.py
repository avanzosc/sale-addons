# Copyright 2025 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    client_order_ref = fields.Char(
        string="Client Reference",
        related="order_id.client_order_ref",
        store=False,
        readonly=True,
    )
