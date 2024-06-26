# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    container = fields.Integer(
        string="Container", related="sale_line_id.container", store=True
    )

    @api.onchange("sale_line_id")
    def onchange_sale_line_id(self):
        self.ensure_one()
        if self.sale_line_id:
            self.container = self.sale_line_id.container
