# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    @api.multi
    def action_confirm(self):
        for order in self:
            if ((not order.expected_delivery_date and any(order.mapped(
                    'order_line.expected_delivery_date'))) or
                    (not order.expected_end_date and any(order.mapped(
                    'order_line.expected_end_date')))):
                raise ValidationError(_('Missing dates'))
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if any(order.mapped('order_line.rental_days')):
                for picking in order.picking_ids.filtered(
                        lambda p: p.state not in ('done', 'cancel')):
                    picking._return_rental()
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    expected_delivery_date = fields.Date(
        string='Expected Delivery Date')
    expected_end_date = fields.Date(
        string='Expected Return Date')
    rental_days = fields.Integer(
        string='Rental Days', compute='_compute_rental_days', store=True)

    @api.depends('expected_delivery_date', 'expected_end_date')
    def _compute_rental_days(self):
        for line in self.filtered(
                lambda l: l.expected_delivery_date and l.expected_end_date):
            line.rental_days = (
                line.expected_end_date - line.expected_delivery_date).days + 1

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id',
                 'rental_days')
    def _compute_amount(self):
        for line in self:
            if line.rental_days:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_id.compute_all(
                    price, line.order_id.currency_id,
                    line.product_uom_qty * line.rental_days,
                    product=line.product_id,
                    partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(
                        t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
            else:
                super(SaleOrderLine, line)._compute_amount()

    @api.constrains('expected_delivery_date', 'expected_end_date')
    def _check_expected_dates(self):
        for line in self.filtered(
                lambda l: l.expected_delivery_date or l.expected_end_date):
            if ((line.expected_delivery_date and not line.expected_end_date)
                    or (line.expected_end_date and
                        not line.expected_delivery_date)):
                raise ValidationError(_('There must be expected delivery '
                                        'date and expected end date.'))
            if line.expected_delivery_date > line.expected_end_date:
                raise ValidationError(_('Expected end date must be after '
                                        'expected delivery date.'))
