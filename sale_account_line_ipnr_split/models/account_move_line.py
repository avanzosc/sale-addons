# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    x_ipnr_gross_price_unit = fields.Float(
        string="Unit price including IPNR",
        store=True,
        copy=True,
        help="Original unit price before IPNR breakdown (IPNR included). "
        "It is used to reverse the breakdown.",
    )
    x_ipnr_parent_line_id = fields.Many2one(
        comodel_name="account.move.line",
        string="Parent invoice line ID",
        store=True,
        help="Bill line to which this IPNR line belongs.",
    )
