# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    sale_price_type = fields.Selection(
        selection=[
            ("sale", "Last Sale Price"),
            ("invoice", "Last Invoice Price"),
            ("pricelist", "Sale Pricelist"),
        ],
        string="Sale Price Type",
        default="pricelist",
        copy=False,
        required=True,
    )
