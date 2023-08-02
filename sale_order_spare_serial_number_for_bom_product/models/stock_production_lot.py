# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models, _


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    sale_line_ids = fields.One2many(
        string="Sale lines", comodel_name="sale.order.line",
        inverse_name="spare_serial_number_id", copy=False)
    count_sale_lines = fields.Integer(
        string="Count sale lines",
        compute="_compute_count_sale_lines")

    def _compute_count_sale_lines(self):
        for lot in self:
            lot.count_sale_lines = len(lot.sale_line_ids)

    def action_sale_lines_from_lot(self):
        self.ensure_one()
        if not self.sale_line_ids:
            return True
        action_window = {
            "name": _("Sale order lines"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order.line",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.sale_line_ids.ids)],
        }
        return action_window
