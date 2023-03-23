# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    amount_pending_invoicing_with_discount = fields.Monetary(
        string="Pending Invoicing Amount With Discount",
        copy=False,
        compute="_compute_amount_pending_invoicing_with_discount",
        store=True,
    )

    @api.depends("price_subtotal", "qty_invoiced")
    def _compute_amount_pending_invoicing_with_discount(self):
        for line in self:
            line.amount_pending_invoicing_with_discount = (
                line.price_subtotal - line.qty_invoiced)
