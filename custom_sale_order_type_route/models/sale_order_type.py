# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    not_route_type = fields.Boolean(
        string="Not Route Type",
        default=False,
    )
    burden_picking_type = fields.Many2one(
        string="Burden Picking Type",
        comodel_name="stock.picking.type"
    )
