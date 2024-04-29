# -*- coding: utf-8 -*-
# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    revised_price = fields.Boolean(
        string='Revised price', compute='_compute_revised_price',
        copy=False, store=True)

    @api.depends("sale_line_id", "sale_line_id.order_id",
                 "sale_line_id.order_id.revised_price")
    def _compute_revised_price(self):
        for move in self.filtered(
                lambda x: x.sale_line_id and x.sale_line_id.order_id):
            move.revised_price = move.sale_line_id.order_id.revised_price
