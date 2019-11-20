# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    expected_delivery_date = fields.Date(
        string='Expected Delivery Date', compute='_compute_rental_days',
        inverse='_inverse_expected_dates', store=True)
    expected_end_date = fields.Date(
        string='Expected Return Date', compute='_compute_rental_days',
        inverse='_inverse_expected_dates', store=True)
    rental_days = fields.Integer(
        string='Rental Days', compute='_compute_rental_days', store=True)

    @api.depends('order_line.expected_delivery_date',
                 'order_line.expected_end_date')
    def _compute_rental_days(self):
        for order in self.filtered('order_line'):
            lines = order.order_line.filtered(
                lambda l: l.expected_delivery_date and l.expected_end_date)
            if lines:
                order.expected_delivery_date = min(lines.mapped(
                    'expected_delivery_date'))
                order.expected_end_date = max(lines.mapped(
                    'expected_end_date'))
                if order.expected_delivery_date and order.expected_end_date:
                    order.rental_days = ((
                        order.expected_end_date -
                        order.expected_delivery_date).days + 1)

    @api.onchange('expected_delivery_date')
    def _onchange_expected_delivery_date(self):
        self.commitment_date = (fields.Datetime.to_datetime(
            self.expected_delivery_date) if self.expected_delivery_date else
            self.commitment_date)

    @api.multi
    def _inverse_expected_dates(self):
        for order in self:
            order_lines = order.order_line.filtered(
                lambda l: l.expected_delivery_date and l.expected_end_date)
            order_lines.write({
                'expected_delivery_date': order.expected_delivery_date,
                'expected_end_date': order.expected_end_date,
            })
            if order.expected_delivery_date and order.expected_end_date:
                order.rental_days = ((order.expected_end_date -
                                      order.expected_delivery_date).days + 1)

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if any(order.mapped('order_line.rental_days')):
                for picking in order.picking_ids.filtered(
                        lambda p: p.state not in ('done', 'cancel')):
                    picking._return_rental()
        return res
