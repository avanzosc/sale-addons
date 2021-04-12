# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(
        string="Commitment Date", related="order_id.commitment_date",
        help="This is the delivery date promised to the customer. If set, the "
             "delivery order will be scheduled based on this date rather than "
             "product lead times.", store=True)
