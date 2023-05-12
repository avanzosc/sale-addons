# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_force_done_detailed_operations(self):
        result = super(StockPicking, self).button_force_done_detailed_operations()
        for line in self.move_line_ids_without_package:
            line.onchange_move_id()
        return result
