# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_order_id = fields.Many2one(
        string='Sale order', comodel_name='sale.order')
    expected_delivery_date = fields.Date(
        string='Expected delivery date',
        related='sale_order_id.expected_delivery_date')
    expected_end_date = fields.Date(
        string='Expected end date', related='sale_order_id.expected_end_date')
    rental_days = fields.Integer(
        string='rental days', related='sale_order_id.rental_days')

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        round_curr = self.currency_id.round
        for line in self.invoice_line_ids:
            if not line.account_id:
                continue
            price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            if line.rental_days:
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit, self.currency_id,
                    line.quantity * line.rental_days,
                    line.product_id, self.partner_id)['taxes']
            else:
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit, self.currency_id, line.quantity,
                    line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(
                    tax['id']).get_grouping_key(val)
                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]['base'] = round_curr(val['base'])
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += round_curr(val['base'])
        return tax_grouped


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    expected_delivery_date = fields.Date(
        string='Expected delivery date',
        compute='_compute_expected_delivery_date', store=True)
    expected_end_date = fields.Date(
        string='Expected end date',
        compute='_compute_expected_end_date', store=True)
    rental_days = fields.Integer(
        string='Rental days',
        compute='_compute_rental_days', store=True)

    @api.depends('sale_line_ids', 'sale_line_ids.expected_delivery_date')
    def _compute_expected_delivery_date(self):
        for line in self:
            for sale_line in line.sale_line_ids.filtered(
                    lambda l: l.expected_delivery_date):
                line.expected_delivery_date = sale_line.expected_delivery_date

    @api.depends('sale_line_ids', 'sale_line_ids.expected_end_date')
    def _compute_expected_end_date(self):
        for line in self:
            for sale_line in line.sale_line_ids.filtered(
                    lambda l: l.expected_end_date):
                line.expected_end_date = sale_line.expected_end_date

    @api.depends('sale_line_ids', 'sale_line_ids.rental_days')
    def _compute_rental_days(self):
        for line in self:
            for sale_line in line.sale_line_ids.filtered(
                    lambda l: l.rental_days):
                line.rental_days = sale_line.rental_days

    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'rental_days', 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        for line in self:
            if line.rental_days:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.invoice_line_tax_ids.compute_all(
                    price, line.invoice_id.currency_id,
                    line.quantity * line.rental_days,
                    product=line.product_id,
                    partner=line.invoice_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(
                        t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
            else:
                super(AccountInvoiceLine, line)._compute_price()
