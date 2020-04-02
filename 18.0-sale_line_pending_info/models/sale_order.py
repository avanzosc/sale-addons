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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered', 'price_unit', 'discount')
    def _compute_qty_amount_pending_delivery(self):
        for line in self:
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
    team_id = fields.Many2one(
        string='Sales team', comodel_name='crm.team', store=True,
        related='order_id.team_id')
