# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_ipnr_gross_price_unit = fields.Float(
        string="Original unit price (with IPNR)",
        store=True,
        copy=True,
        help="Original unit price before IPNR breakdown (IPNR included). "
        "It is used to reverse the breakdown and to transfer the gross price to the invoice.",
    )
    x_ipnr_parent_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        ondelete="set null",
        string="Parent order line ID",
        store=True,
        help="Sales order line to which this IPNR line belongs.",
    )
