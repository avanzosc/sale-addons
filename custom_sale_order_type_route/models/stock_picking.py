# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_carry_type = fields.Boolean(
        string="Carry Type",
        related="picking_type_id.is_carry_type",
        store=True
    )
