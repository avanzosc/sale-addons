# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    sale_type_id = fields.Many2one(
        string="Sale type",
        comodel_name="sale.order.type",
        related="picking_id.sale_type_id",
        store=True,
        copy=False,
    )

    picking_type_code = fields.Selection(related="picking_id.picking_type_code")
