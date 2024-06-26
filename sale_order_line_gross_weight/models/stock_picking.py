# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        result = super(StockPicking, self).button_force_done_detailed_operations()
        for picking in self:
            for line in picking.move_line_ids_without_package:
                if line.move_id and line.move_id.sale_line_id:
                    line.gross_weight = line.move_id.sale_line_id.gross_weight
        return result
