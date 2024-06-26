# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    filter_lot_by_location = fields.Boolean(
        string="Filter Lot By Location", default=True
    )
