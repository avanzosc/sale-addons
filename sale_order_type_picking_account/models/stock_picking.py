# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_type_id = fields.Many2one(
        string="Sale type",
        comodel_name="sale.order.type",
        related="group_id.sale_id.type_id",
        store=True,
        copy=False,
    )
