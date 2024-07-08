# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_qty_pending_delivery = fields.Float(
        string="Pending Delivery Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_total_qty_amount_pending_delivery",
        store=True,
    )
    total_amount_pending_delivery = fields.Monetary(
        string="Pending Delivery Amount",
        copy=False,
        compute="_compute_total_qty_amount_pending_delivery",
        store=True,
    )
    total_qty_pending_invoicing = fields.Float(
        string="Pending Invoicing Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_total_qty_amount_pending_invoicing",
        store=True,
    )
    total_amount_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Amount",
        copy=False,
        compute="_compute_total_qty_amount_pending_invoicing",
        store=True,
    )
    total_qty_shipped_pending_invoicing = fields.Float(
        string="Pending Invoicing Shipped Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_total_qty_shipped_pending_invoicing",
        store=True,
    )
    total_amount_shipped_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Shipped Amount",
        copy=False,
        compute="_compute_total_qty_shipped_pending_invoicing",
        store=True,
    )

    @api.depends(
        "order_line",
        "order_line.amount_pending_delivery",
        "order_line.qty_pending_delivery",
    )
    def _compute_total_qty_amount_pending_delivery(self):
        for sale in self:
            sale.total_amount_pending_delivery = sum(
                sale.order_line.mapped("amount_pending_delivery")
            )
            sale.total_qty_pending_delivery = sum(
                sale.order_line.mapped("qty_pending_delivery")
            )

    @api.depends(
        "order_line",
        "order_line.amount_pending_invoicing",
        "order_line.qty_pending_invoicing",
    )
    def _compute_total_qty_amount_pending_invoicing(self):
        for sale in self:
            sale.total_amount_pending_invoicing = sum(
                sale.order_line.mapped("amount_pending_invoicing")
            )
            sale.total_qty_pending_invoicing = sum(
                sale.order_line.mapped("qty_pending_invoicing")
            )

    @api.depends(
        "order_line",
        "order_line.qty_shipped_pending_invoicing",
        "order_line.amount_pending_invoicing",
    )
    def _compute_total_qty_shipped_pending_invoicing(self):
        for sale in self:
            sale.total_qty_shipped_pending_invoicing = sum(
                sale.order_line.mapped("qty_shipped_pending_invoicing")
            )
            sale.total_amount_shipped_pending_invoicing = sum(
                sale.order_line.mapped("amount_shipped_pending_invoicing")
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    qty_pending_delivery = fields.Float(
        string="Pending Delivery Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_amount_pending_delivery",
        store=True,
    )
    amount_pending_delivery = fields.Monetary(
        string="Pending Delivery Amount",
        copy=False,
        compute="_compute_qty_amount_pending_delivery",
        store=True,
    )
    qty_pending_invoicing = fields.Float(
        string="Pending Invoicing Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_amount_pending_invoicing",
        store=True,
    )
    amount_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Amount",
        copy=False,
        compute="_compute_qty_amount_pending_invoicing",
        store=True,
    )
    qty_shipped_pending_invoicing = fields.Float(
        string="Pending Invoicing Shipped Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_shipped_pending_invoicing",
        store=True,
    )
    amount_shipped_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Shipped Amount",
        copy=False,
        compute="_compute_qty_shipped_pending_invoicing",
        store=True,
    )
    team_id = fields.Many2one(
        string="Sales Team",
        comodel_name="crm.team",
        store=True,
        related="order_id.team_id",
    )

    @api.depends(
        "product_uom_qty",
        "qty_delivered_method",
        "qty_delivered",
        "price_unit",
        "discount",
    )
    def _compute_qty_amount_pending_delivery(self):
        for line in self:
            qty_pending_delivery = amount_pending_delivery = 0
            if line.qty_delivered_method == "stock_move":
                qty_pending_delivery = line.product_uom_qty - line.qty_delivered
                if qty_pending_delivery < 0:
                    qty_pending_delivery = 0
                amount = qty_pending_delivery * line.price_unit
                if line.discount:
                    amount -= (amount * line.discount) / 100
                amount_pending_delivery = amount
            line.qty_pending_delivery = qty_pending_delivery
            line.amount_pending_delivery = amount_pending_delivery

    @api.depends(
        "product_uom_qty",
        "qty_invoiced",
        "discount",
        "price_unit",
    )
    def _compute_qty_amount_pending_invoicing(self):
        for line in self:
            line.qty_pending_invoicing = line.product_uom_qty - line.qty_invoiced
            amount = line.qty_pending_invoicing * line.price_unit
            if line.discount:
                amount -= (amount * line.discount) / 100
            line.amount_pending_invoicing = amount

    @api.depends(
        "qty_delivered",
        "qty_invoiced",
        "discount",
        "price_unit",
    )
    def _compute_qty_shipped_pending_invoicing(self):
        for line in self:
            amount = 0
            qty = line.qty_delivered - line.qty_invoiced
            if qty > 0:
                amount = qty * line.price_unit
                amount -= (amount * line.discount) / 100 if line.discount else 0
            line.qty_shipped_pending_invoicing = qty if qty > 0 else 0
            line.amount_shipped_pending_invoicing = amount
