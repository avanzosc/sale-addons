# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    remain_amount = fields.Float(string='Remaining amount',
                                 compute='_compute_remaining_credit')
    remain_quantity = fields.Float(string='Remaining quantity',
                                   compute='_compute_remaining_credit')

    def _compute_remaining_credit(self):
        for partner in self:
            limits = partner.check_actual_limits()
            remain_amount = remain_quantity = 0
            if partner.property_product_pricelist.has_limit:
                remain_amount = (
                    partner.property_product_pricelist.limit_amount -
                    limits['actual_amount'])
                remain_quantity = (
                    partner.property_product_pricelist.limit_qty -
                    limits['actual_qty'])
            partner.remain_amount = remain_amount
            partner.remain_quantity = remain_quantity

    def check_actual_limits(self):
        move_obj = self.env['stock.move']
        location_obj = self.env['stock.location']
        internal_ids = location_obj.search([('usage', '=', 'internal')]).ids
        negative_moves = move_obj.search([
            ('partner_id', '=', self.id),
            ('location_id', 'in', internal_ids),
            ('location_dest_id', 'not in', internal_ids),
            ('state', '!=', 'cancel')]).filtered(
            lambda x: x.sale_line_id and
            x.sale_line_id.order_id.pricelist_id.has_limit)
        negative_amount = sum([x.product_price for x in negative_moves])
        negative_qty = sum([x.product_uom_qty for x in negative_moves])
        positive_moves = move_obj.search([
            ('partner_id', '=', self.id),
            ('location_id', 'not in', internal_ids),
            ('location_dest_id', 'in', internal_ids),
            ('state', '!=', 'cancel')])
        positive_amount = sum([x.product_price for x in positive_moves
                               if x.picking_id.stock_return_confirm])
        positive_qty = sum([x.product_uom_qty for x in positive_moves
                            if x.picking_id.stock_return_confirm])
        return {'actual_amount': negative_amount - positive_amount,
                'actual_qty': negative_qty - positive_qty
                }
