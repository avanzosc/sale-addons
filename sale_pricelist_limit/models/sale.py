# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    no_discount_price = fields.Float(string='Real price',
                                     compute='_compute_real_price')

    def _compute_real_price(self):
        for order in self:
            amount = 0
            for line in order.order_line.filtered(
                    lambda x: x.product_id.product_tmpl_id.type != 'service'):
                amount = amount + \
                    line.product_id.lst_price * line.product_uom_qty
            order.no_discount_price = amount

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.pricelist_id.has_limit:
                limits = order.partner_id.check_actual_limits()
                limit_credit = (
                    order.pricelist_id.limit_amount -
                    (order.no_discount_price + limits['actual_amount']))
                total_qty = sum(order.order_line.filtered(
                    lambda x: x.product_id.product_tmpl_id.type != 'service').
                    mapped('product_uom_qty'))
                limit_qty = (
                    order.pricelist_id.limit_qty -
                    (total_qty + limits['actual_qty']))
                if limit_credit < 0:
                    raise exceptions.Warning(
                        _(u'Sale amount exceeded pricelist limit by: {}'.
                          format(abs(limit_credit))))
                elif limit_qty < 0:
                    raise exceptions.Warning(
                        _(u'Sale quantity exceeded pricelist limit by: {}'.
                          format(abs(limit_qty))))
        return super(SaleOrder, self).action_confirm()
