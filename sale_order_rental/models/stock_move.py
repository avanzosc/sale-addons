# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    expected_delivery_date = fields.Date(
        string='Expected Delivery Date',
        related='sale_line_id.expected_delivery_date',
        inverse='_inverse_expected_dates',
        store=True)
    expected_end_date = fields.Date(
        string='Expected Return Date',
        related='sale_line_id.expected_end_date',
        inverse='_inverse_expected_dates',
        store=True)
    rental_days = fields.Integer(
        string='Rental Days', compute='_compute_rental_days', store=True)

    @api.depends('expected_delivery_date', 'expected_end_date')
    def _compute_rental_days(self):
        for line in self.filtered(lambda l: l.expected_delivery_date and
                                  l.expected_end_date):
            line.rental_days = ((
                line.expected_end_date - line.expected_delivery_date).days + 1)

    @api.multi
    def _inverse_expected_dates(self):
        for line in self.filtered('sale_line_id'):
            line.sale_line_id.write({
                'expected_delivery_date': line.expected_delivery_date,
                'expected_end_date': line.expected_end_date,
            })

    @api.constrains('expected_delivery_date', 'expected_end_date')
    def _check_expected_dates(self):
        for line in self.filtered(
                lambda l: l.expected_delivery_date or l.expected_end_date):
            if ((line.expected_delivery_date and not line.expected_end_date)
                    or (line.expected_end_date and not
                        line.expected_delivery_date)):
                raise ValidationError(_('There must be expected delivery '
                                        'date and expected end date.'))
            if line.expected_delivery_date > line.expected_end_date:
                raise ValidationError(_('Expected end date must be after '
                                        'expected delivery date.'))
