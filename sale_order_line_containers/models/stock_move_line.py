# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    container = fields.Integer(string="Container")

    @api.onchange("move_id")
    def onchange_move_id(self):
        self.ensure_one()
        if self.move_id:
            self.container = self.move_id.container
