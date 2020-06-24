# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.depends('order_line', 'order_line.amount_pending_delivery',
                 'order_line.qty_pending_delivery')
    def _compute_total_qty_amount_pending_delivery(self):
        for sale in self:
            sale.total_amount_pending_delivery = sum(
                sale.order_line.mapped('amount_pending_delivery'))
            sale.total_qty_pending_delivery = sum(
                sale.order_line.mapped('qty_pending_delivery'))

    @api.multi
    @api.depends('order_line', 'order_line.amount_pending_invoicing',
                 'order_line.qty_pending_invoicing')
    def _compute_total_qty_amount_pending_invoicing(self):
        for sale in self:
            sale.total_amount_pending_invoicing = sum(
                sale.order_line.mapped('amount_pending_invoicing'))
            sale.total_qty_pending_invoicing = sum(
                sale.order_line.mapped('qty_pending_invoicing'))

    @api.multi
    @api.depends('order_line', 'order_line.qty_shipped_pending_invoicing',
                 'order_line.amount_pending_invoicing')
    def _compute_total_qty_shipped_pending_invoicing(self):
        for sale in self:
            sale.total_qty_shipped_pending_invoicing = sum(
                sale.order_line.mapped('qty_shipped_pending_invoicing'))
            sale.total_amount_shipped_pending_invoicing = sum(
                sale.order_line.mapped('amount_shipped_pending_invoicing'))

    total_qty_pending_delivery = fields.Float(
        string='Total pending delivery qty', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_total_qty_amount_pending_delivery', store=True)
    total_amount_pending_delivery = fields.Monetary(
        string='Total amount pending delivery', copy=False,
        compute='_compute_total_qty_amount_pending_delivery', store=True)
    total_qty_pending_invoicing = fields.Float(
        string='Total pending invoicing qty', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_total_qty_amount_pending_invoicing', store=True)
    total_amount_pending_invoicing = fields.Monetary(
        string='Total amount pending invoicing', copy=False,
        compute='_compute_total_qty_amount_pending_invoicing', store=True)
    total_qty_shipped_pending_invoicing = fields.Float(
        string='Total Qty shipped pending invoicing', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_total_qty_shipped_pending_invoicing', store=True)
    total_amount_shipped_pending_invoicing = fields.Monetary(
        string='Total amount shipped pending invoicing', copy=False,
        compute='_compute_total_qty_shipped_pending_invoicing', store=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered', 'price_unit', 'discount',
                 'order_id', 'order_id.picking_ids',
                 'order_id.picking_ids.state')
    def _compute_qty_amount_pending_delivery(self):
        for line in self:
            found = False
            for picking in line.order_id.picking_ids:
                if any([x.state not in ('done', 'cancel') and
                        x.product_id.id == line.product_id.id for x in
                        picking.move_lines]):
                    found = True
            if not found or line.product_id.type == 'service':
                line.amount_pending_delivery = 0
            if found:
                line.qty_pending_delivery = (
                    line.product_uom_qty - line.qty_delivered)
                amount = line.qty_pending_delivery * line.price_unit
                if line.discount:
                    amount -= (amount * line.discount) / 100
                line.amount_pending_delivery = amount

    @api.multi
    @api.depends('product_uom_qty', 'qty_invoiced', 'discount')
    def _compute_qty_amount_pending_invoicing(self):
        for line in self:
            line.qty_pending_invoicing = (
                line.product_uom_qty - line.qty_invoiced)
            amount = line.qty_pending_invoicing * line.price_unit
            if line.discount:
                amount -= (amount * line.discount) / 100
            line.amount_pending_invoicing = amount

    @api.multi
    @api.depends('qty_delivered', 'qty_invoiced', 'discount', 'price_unit')
    def _compute_qty_shipped_pending_invoicing(self):
        for line in self:
            amount = 0
            qty = line.qty_delivered - line.qty_invoiced
            if qty > 0:
                amount = qty * line.price_unit
                amount -= (
                    (amount * line.discount) / 100 if line.discount else 0)
            line.qty_shipped_pending_invoicing = qty if qty > 0 else 0
            line.amount_shipped_pending_invoicing = amount

    qty_pending_delivery = fields.Float(
        string='Pending delivery qty', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_qty_amount_pending_delivery', store=True)
    amount_pending_delivery = fields.Monetary(
        string='Amount pending delivery', copy=False,
        compute='_compute_qty_amount_pending_delivery', store=True)
    qty_pending_invoicing = fields.Float(
        string='Pending invoicing qty', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_qty_amount_pending_invoicing', store=True)
    amount_pending_invoicing = fields.Monetary(
        string='Amount pending invoicing', copy=False,
        compute='_compute_qty_amount_pending_invoicing', store=True)
    qty_shipped_pending_invoicing = fields.Float(
        string='Qty shipped pending invoicing', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_compute_qty_shipped_pending_invoicing', store=True)
    amount_shipped_pending_invoicing = fields.Monetary(
        string='Amount shipped pending invoicing', copy=False,
        compute='_compute_qty_shipped_pending_invoicing', store=True)
    team_id = fields.Many2one(
        string='Sales team', comodel_name='crm.team', store=True,
        related='order_id.team_id')
