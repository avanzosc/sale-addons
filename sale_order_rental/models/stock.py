# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    expected_delivery_date = fields.Date(
        related='sale_id.expected_delivery_date')
    expected_end_date = fields.Date(
        string='Expected end date', related='sale_id.expected_end_date')
    rental_days = fields.Integer(
        related='sale_id.rental_days')


class StockMove(models.Model):
    _inherit = 'stock.move'

    expected_delivery_date = fields.Date(
        related='sale_line_id.expected_delivery_date', readonly=False)
    expected_end_date = fields.Date(
        string='Expected end date',
        related='sale_line_id.expected_end_date', readonly=False)
    rental_days = fields.Integer(
        related='sale_line_id.rental_days')
