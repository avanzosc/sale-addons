# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sale_order_id = fields.Many2one(
        string='Sale order', comodel_name='sale.order')
    sale_expected_delivery_date = fields.Date(
        string='Expected Delivery Date',
        compute='_compute_rental_dates', store=True)
    sale_expected_end_date = fields.Date(
        string='Expected Return Date',
        compute='_compute_rental_dates', store=True)
    rental_days = fields.Integer(
        string='Rental Days',
        compute='_compute_rental_dates', store=True)

    @api.depends('invoice_line_ids',
                 'invoice_line_ids.sale_expected_delivery_date',
                 'invoice_line_ids.sale_expected_end_date')
    def _compute_rental_dates(self):
        for invoice in self.filtered('invoice_line_ids'):
            lines = invoice.invoice_line_ids.filtered(
                lambda l: l.sale_expected_delivery_date or
                l.sale_expected_end_date)
            if lines:
                invoice.sale_expected_delivery_date = min(lines.mapped(
                    'sale_expected_delivery_date'))
                invoice.sale_expected_end_date = max(lines.mapped(
                    'sale_expected_end_date'))
                invoice.rental_days = ((
                    invoice.sale_expected_end_date -
                    invoice.sale_expected_delivery_date).days + 1)

    @api.multi
    def get_taxes_values(self):
        tax_grouped = super(AccountInvoice, self).get_taxes_values()
        if any(self.invoice_line_ids.filtered('rental_days')):
            tax_grouped = {}
            round_curr = self.currency_id.round
            for line in self.invoice_line_ids:
                if not line.account_id:
                    continue
                price_unit = line.price_unit * (
                    1 - (line.discount or 0.0) / 100.0)
                quantity = line.quantity
                if line.rental_days:
                    quantity *= line.rental_days
                taxes = line.invoice_line_tax_ids.compute_all(
                    price_unit, self.currency_id, quantity, line.product_id,
                    self.partner_id)['taxes']
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
