# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        for sale in self:
            for picking in sale.picking_ids:
                for move in picking.move_ids_without_package:
                    if move.sale_line_id:
                        for line in move.move_line_ids:
                            line.gross_weight = move.sale_line_id.gross_weight
        return result
