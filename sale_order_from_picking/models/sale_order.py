# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    picking_from_id = fields.Many2one(comodel_name='stock.picking',
                                      string='From Picking')
    picking_ref = fields.Char(related="picking_from_id.name")
    picking_scheduled_date = fields.Datetime(
        related="picking_from_id.scheduled_date")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    stock_move_id = fields.Many2one(comodel_name='stock.move', string='Move')
