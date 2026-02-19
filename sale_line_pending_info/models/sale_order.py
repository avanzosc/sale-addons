# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# Copyright 2026 Eñaut Alberdi - AvanzOSC
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
        readonly=True,
    )
    total_amount_pending_delivery = fields.Monetary(
        string="Pending Delivery Amount",
        copy=False,
        compute="_compute_total_qty_amount_pending_delivery",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    total_qty_pending_invoicing = fields.Float(
        string="Pending Invoicing Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_total_qty_amount_pending_invoicing",
        store=True,
        readonly=True,
    )
    total_amount_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Amount",
        copy=False,
        compute="_compute_total_qty_amount_pending_invoicing",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    total_qty_shipped_pending_invoicing = fields.Float(
        string="Pending Invoicing Shipped Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_total_qty_shipped_pending_invoicing",
        store=True,
        readonly=True,
    )
    total_amount_shipped_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Shipped Amount",
        copy=False,
        compute="_compute_total_qty_shipped_pending_invoicing",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    qty_ordered = fields.Float(
        string="Total Units Ordered",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_ordered",
        store=True,
        readonly=True,
    )
    qty_delivered = fields.Float(
        string="Total Qty Delivered",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_delivered",
        store=True,
        readonly=True,
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
        "order_line.amount_shipped_pending_invoicing",
    )
    def _compute_total_qty_shipped_pending_invoicing(self):
        for sale in self:
            sale.total_qty_shipped_pending_invoicing = sum(
                sale.order_line.mapped("qty_shipped_pending_invoicing")
            )
            sale.total_amount_shipped_pending_invoicing = sum(
                sale.order_line.mapped("amount_shipped_pending_invoicing")
            )

    @api.depends("order_line", "order_line.state", "order_line.product_uom_qty")
    def _compute_qty_ordered(self):
        for sale in self:
            sale.qty_ordered = sum(
                sale.order_line.filtered(lambda x: x.state != "cancel").mapped(
                    "product_uom_qty"
                )
            )

    @api.depends("order_line", "order_line.state", "order_line.qty_delivered")
    def _compute_qty_delivered(self):
        for sale in self:
            sale.qty_delivered = sum(
                sale.order_line.filtered(lambda x: x.state != "cancel").mapped(
                    "qty_delivered"
                )
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    qty_pending_delivery = fields.Float(
        string="Pending Delivery Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_amount_pending_delivery",
        store=True,
        readonly=True,
    )
    amount_pending_delivery = fields.Monetary(
        string="Pending Delivery Amount",
        copy=False,
        compute="_compute_qty_amount_pending_delivery",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    qty_pending_invoicing = fields.Float(
        string="Pending Invoicing Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_amount_pending_invoicing",
        store=True,
        readonly=True,
    )
    amount_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Amount",
        copy=False,
        compute="_compute_qty_amount_pending_invoicing",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    qty_shipped_pending_invoicing = fields.Float(
        string="Pending Invoicing Shipped Qty",
        copy=False,
        digits="Product Unit of Measure",
        compute="_compute_qty_shipped_pending_invoicing",
        store=True,
        readonly=True,
    )
    amount_shipped_pending_invoicing = fields.Monetary(
        string="Pending Invoicing Shipped Amount",
        copy=False,
        compute="_compute_qty_shipped_pending_invoicing",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )
    team_id = fields.Many2one(
        string="Sales Team",
        comodel_name="crm.team",
        store=True,
        related="order_id.team_id",
        readonly=True,
    )

    @api.depends(
        "product_uom_qty",
        "qty_delivered",
        "price_unit",
        "discount",
        "product_id.type",
        "order_id.picking_ids",
        "order_id.picking_ids.state",
        "order_id.picking_ids.move_ids.state",
        "order_id.picking_ids.move_ids.product_id",
    )
    def _compute_qty_amount_pending_delivery(self):
        for line in self:
            product_id = line.product_id.id
            found = bool(
                line.order_id.picking_ids.move_ids.filtered_domain(
                    [
                        ("state", "not in", ("done", "cancel")),
                        ("product_id", "=", product_id),
                    ]
                )
            )
            if not found or line.product_id.type == "service":
                line.qty_pending_delivery = 0.0
                line.amount_pending_delivery = 0.0
                continue
            line.qty_pending_delivery = line.product_uom_qty - line.qty_delivered
            amount = line.qty_pending_delivery * line.price_unit
            amount *= 1 - (line.discount or 0.0) / 100.0
            line.amount_pending_delivery = amount

    @api.depends(
        "product_uom_qty",
        "qty_invoiced",
        "discount",
        "price_unit",
    )
    def _compute_qty_amount_pending_invoicing(self):
        for line in self:
            qty_pending_invoicing = line.product_uom_qty - line.qty_invoiced
            amount = qty_pending_invoicing * line.price_unit
            amount *= 1 - (line.discount or 0.0) / 100.0
            line.qty_pending_invoicing = qty_pending_invoicing
            line.amount_pending_invoicing = amount

    @api.depends(
        "qty_delivered",
        "qty_invoiced",
        "discount",
        "price_unit",
    )
    def _compute_qty_shipped_pending_invoicing(self):
        for line in self:
            qty = max(line.qty_delivered - line.qty_invoiced, 0.0)
            amount = qty * line.price_unit
            amount *= 1 - (line.discount or 0.0) / 100.0
            line.qty_shipped_pending_invoicing = qty
            line.amount_shipped_pending_invoicing = amount
