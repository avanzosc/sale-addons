# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    sale_expected_delivery_date = fields.Date(
        string='Expected Delivery Date',
        compute='_compute_sale_rental_dates', store=True)
    sale_expected_end_date = fields.Date(
        string='Expected Return Date',
        compute='_compute_sale_rental_dates', store=True)
    rental_days = fields.Integer(
        string='Rental Days',
        compute='_compute_sale_rental_dates', store=True)

    @api.depends('sale_line_ids',
                 'sale_line_ids.expected_delivery_date',
                 'sale_line_ids.expected_end_date',
                 'sale_line_ids.rental_days')
    def _compute_sale_rental_dates(self):
        for line in self.filtered('sale_line_ids'):
            sale_lines = line.sale_line_ids.filtered(
                lambda l: l.expected_delivery_date and
                l.expected_end_date)
            if sale_lines:
                line.sale_expected_delivery_date = min(sale_lines.mapped(
                    'expected_delivery_date'))
                line.sale_expected_end_date = max(sale_lines.mapped(
                    'expected_end_date'))
                line.rental_days = sum(sale_lines.mapped('rental_days'))

    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'rental_days', 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        for line in self:
            if line.rental_days:
                currency = (
                    line.invoice_id and line.invoice_id.currency_id or None)
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = False
                quantity = line.quantity * line.rental_days
                if line.invoice_line_tax_ids:
                    taxes = line.invoice_line_tax_ids.compute_all(
                        price, currency, quantity, product=line.product_id,
                        partner=line.invoice_id.partner_id)
                line.price_subtotal = price_subtotal_signed = taxes[
                    'total_excluded'] if taxes else quantity * price
                line.price_total = taxes[
                    'total_included'] if taxes else line.price_subtotal
                if (line.invoice_id.currency_id and
                        line.invoice_id.currency_id !=
                        line.invoice_id.company_id.currency_id):
                    currency = line.invoice_id.currency_id
                    date = line.invoice_id._get_currency_rate_date()
                    price_subtotal_signed = currency._convert(
                        price_subtotal_signed,
                        line.invoice_id.company_id.currency_id,
                        line.company_id or line.env.user.company_id,
                        date or fields.Date.today())
                sign = line.invoice_id.type in ['in_refund',
                                                'out_refund'] and -1 or 1
                line.price_subtotal_signed = price_subtotal_signed * sign
            else:
                super(AccountInvoiceLine, line)._compute_price()
