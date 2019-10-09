# Copyright 2019 Oihana Larrañaga - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    expected_delivery_date = fields.Date(
        string='Expected Delivery Date',
        related='sale_id.expected_delivery_date')
    expected_end_date = fields.Date(
        string='Expected Return Date', related='sale_id.expected_end_date')
    rental_days = fields.Integer(
        related='sale_id.rental_days')

    @api.multi
    def _return_rental(self):
        self.ensure_one()
        if self.state == 'cancel':
            return
        res = {'picking_id': self.id}
        product_return_moves = []
        move_dest_exists = False
        for move in self.move_lines.filtered('sale_line_id.rental_days'):
            if move.scrapped:
                continue
            if move.move_dest_ids:
                move_dest_exists = True
            quantity = move.product_qty - sum(move.move_dest_ids.filtered(
                lambda m: m.state in ['partially_available', 'assigned',
                                      'done']).mapped('move_line_ids').mapped(
                'product_qty'))
            quantity = float_round(
                quantity, precision_rounding=move.product_uom.rounding)
            product_return_moves.append(
                (0, 0, {'product_id': move.product_id.id,
                        'quantity': quantity,
                        'move_id': move.id,
                        'uom_id': move.product_id.uom_id.id}))
        if not product_return_moves:
            return
        if self.location_id.usage == 'internal':
            res.update({
                'parent_location_id':
                    (self.picking_type_id.warehouse_id and
                     self.picking_type_id.warehouse_id.view_location_id.id or
                     self.location_id.location_id.id),
            })
        location_id = self.location_id.id
        if self.picking_type_id.return_picking_type_id\
                .default_location_dest_id.return_location:
            location_id = \
                self.picking_type_id.return_picking_type_id\
                    .default_location_dest_id.id
        res.update({
            'product_return_moves': product_return_moves,
            'move_dest_exists': move_dest_exists,
            'original_location_id': self.location_id.id,
            'location_id': location_id,
        })
        return_wiz = self.env['stock.return.picking'].create(res)
        return_wiz._create_returns()
        return True


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

    @api.depends('sale_line_id.expected_delivery_date')
    def _compute_expected_delivery_date(self):
        for line in self.filtered('sale_line_id'):
            line.expected_delivery_date = (
                line.sale_line_id.expected_delivery_date)

    @api.depends('sale_line_id.expected_end_date')
    def _compute_expected_end_date(self):
        for line in self.filtered('sale_line_id'):
            line.expected_end_date = (
                line.sale_line_id.expected_end_date)

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
