# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    burden_partner_id = fields.Many2one(
        string="Burden Partner",
        comodel_name="res.partner",
    )
    surplus = fields.Boolean(default=False)
    is_carry_type = fields.Boolean(related="picking_id.is_carry_type", store=False)
