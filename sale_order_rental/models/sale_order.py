# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    expected_delivery_date = fields.Date(
        string='Expected delivery date')
    expected_end_date = fields.Date(
        string='Expected end date')
    rental_days = fields.Integer(
        string='Rental days', compute='_compute_rental_days', store=True)

    @api.depends('expected_delivery_date', 'expected_end_date')
    def _compute_rental_days(self):
        for order in self.filtered(lambda o: o.expected_delivery_date and
                                   o.expected_end_date):
                order.rental_days = abs(
                    order.expected_end_date-order.expected_delivery_date
                    ).days + 1

    @api.onchange('expected_delivery_date')
    def onchange_expected_delivery_date(self):
        if self.expected_delivery_date:
            self.commitment_date = fields.Datetime.to_datetime(
                self.expected_delivery_date)
            for line in self.order_line:
                line.expected_delivery_date = self.expected_delivery_date

    @api.onchange('expected_end_date')
    def onchange_expected_end_date(self):
        if self.expected_delivery_date > self.expected_end_date:
            raise UserError(
                "Expected end date must be greater "
                "than expected delivery date")
            if self.expected_end_date:
                for line in self.order_line:
                    line.expected_end_date = self.expected_end_date

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            for picking in sale.picking_ids.filtered(
                    lambda l: l.expected_end_date):
                vals = {
                    'location_id': picking.location_dest_id.id,
                    'location_dest_id': picking.location_id.id,
                    'picking_type_id':
                    picking.picking_type_id.return_picking_type_id.id}
                if picking.expected_end_date:
                    vals['scheduled_date'] = (
                        "{} 08:00:00".format(picking.expected_end_date))
                new_picking = picking.copy(vals)
                for move in new_picking.move_lines:
                    if move.expected_end_date:
                        vals = {
                            'location_id': new_picking.location_id.id,
                            'location_dest_id':
                            new_picking.location_dest_id.id}
                        if move.expected_end_date:
                            vals['date_expected'] = (
                                "{} 08:00:00".format(move.expected_end_date))
                        move.write(vals)
                        move._action_confirm()
                    if not move.expected_end_date:
                        move.unlink()
        return res

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['sale_order_id'] = self.id
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    expected_delivery_date = fields.Date(
        string='Expected delivery date')
    expected_end_date = fields.Date(
        string='Expected end date', )
    rental_days = fields.Integer(
        string='Rental days', compute='_compute_rental_days', store=True)

    @api.depends('expected_delivery_date', 'expected_end_date')
    def _compute_rental_days(self):
        for line in self.filtered(lambda l: l.expected_delivery_date and
                                  l.expected_end_date):
            if line.expected_delivery_date > line.expected_end_date:
                raise UserError(
                    "Expected end date must be greater "
                    "than expected delivery date")
            else:
                line.rental_days = abs(
                    line.expected_end_date - line.expected_delivery_date
                    ).days + 1

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.order_id.expected_delivery_date:
            self.expected_delivery_date = self.order_id.expected_delivery_date
        if self.order_id.expected_end_date:
            self.expected_end_date = self.order_id.expected_end_date
        return result

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

    @api.multi
    def invoice_line_create_vals(self, invoice_id, qty):
        res = super(
            SaleOrderLine, self).invoice_line_create_vals(invoice_id, qty)
        for result in res:
            if result.get('sale_line_ids', False):
                a = result.get('sale_line_ids')
                sale_line_id = a[0][2][0]
                if sale_line_id:
                    result['sale_order_line_id'] = sale_line_id
        return res
