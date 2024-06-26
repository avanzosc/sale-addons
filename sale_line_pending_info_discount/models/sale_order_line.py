# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends(
        "product_uom_qty",
        "qty_delivered_method",
        "qty_delivered",
        "price_unit",
        "discount",
        "discount2",
        "discount3",
    )
    def _compute_qty_amount_pending_delivery(self):
        result = super(SaleOrderLine, self)._compute_qty_amount_pending_delivery()
        for line in self:
            qty_pending_delivery = amount_pending_delivery = 0
            if line.qty_delivered_method == "stock_move":
                qty_pending_delivery = line.product_uom_qty - line.qty_delivered
                if qty_pending_delivery < 0:
                    qty_pending_delivery = 0
                amount = qty_pending_delivery * line.price_unit
                if line.discount:
                    amount -= (amount * line.discount) / 100
                if line.discount2:
                    amount -= (amount * line.discount2) / 100
                if line.discount3:
                    amount -= (amount * line.discount3) / 100
                amount_pending_delivery = amount
            line.amount_pending_delivery = amount_pending_delivery
        return result

    @api.depends(
        "product_uom_qty",
        "qty_invoiced",
        "discount",
        "discount2",
        "discount3",
        "price_unit",
    )
    def _compute_qty_amount_pending_invoicing(self):
        result = super(SaleOrderLine, self)._compute_qty_amount_pending_invoicing()
        for line in self:
            amount = line.qty_pending_invoicing * line.price_unit
            if line.discount:
                amount -= (amount * line.discount) / 100
            if line.discount2:
                amount -= (amount * line.discount2) / 100
            if line.discount3:
                amount -= (amount * line.discount3) / 100
            line.amount_pending_invoicing = amount
        return result

    @api.depends(
        "qty_delivered",
        "qty_invoiced",
        "discount",
        "discount2",
        "discount3",
        "price_unit",
    )
    def _compute_qty_shipped_pending_invoicing(self):
        result = super(SaleOrderLine, self)._compute_qty_shipped_pending_invoicing()
        for line in self:
            amount = 0
            qty = line.qty_delivered - line.qty_invoiced
            if qty > 0:
                amount = qty * line.price_unit
                if line.discount:
                    amount -= (amount * line.discount) / 100
                if line.discount2:
                    amount -= (amount * line.discount2) / 100
                if line.discount3:
                    amount -= (amount * line.discount3) / 100
            line.amount_shipped_pending_invoicing = amount
        return result
