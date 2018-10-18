# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, exceptions, fields, models, _
from openerp.addons import decimal_precision as dp


class DuplicateUpgradableSale(models.TransientModel):
    _name = "duplicate.upgradable.sale"

    reserved_quantity = fields.Float(digits=dp.get_precision(
        'Product Unit of Measure'))
    not_reserved_quantity = fields.Float(digits=dp.get_precision(
        'Product Unit of Measure'))
    quantity = fields.Float(digits=dp.get_precision(
        'Product Unit of Measure'))

    @api.model
    def default_get(self, var_fields):
        res = super(DuplicateUpgradableSale, self).default_get(var_fields)
        order = self.env['sale.order'].browse(self._context.get('active_ids'))
        order.ensure_one()
        if not order.upgrade:
            raise exceptions.Warning(_("Order not upgradable"))
        reserved_qty = sum(order.mapped(
            "child_order_ids.order_line.product_uom_qty"))
        total = order.order_line[0].product_uom_qty
        res.update(
            {'reserved_quantity': reserved_qty,
             'not_reserved_quantity': total - reserved_qty}
        )
        return res

    @api.multi
    def action_duplicate(self):
        orders = self.env['sale.order'].browse(self._context.get('active_ids'))
        orders.ensure_one()
        quantity = self.quantity or self.not_reserved_quantity or False
        if not quantity or quantity > self.not_reserved_quantity:
            raise exceptions.Warning(_("Quantity is excessive or order is "
                                       "fully served"))
        orders.action_create_order_from_upgrade(quantity)
