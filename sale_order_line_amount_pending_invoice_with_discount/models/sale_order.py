# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_amount_pending_invoicing_with_discount = fields.Monetary(
        string="Pending Invoicing Amount With Discount",
        copy=False,
        compute="_compute_total_amount_pending_invoicing_with_discount",
        store=True,
    )

    @api.depends("order_line",
                 "order_line.amount_pending_invoicing_with_discount")
    def _compute_total_amount_pending_invoicing_with_discount(self):
        for sale in self:
            sale.total_amount_pending_invoicing_with_discount = (
                sum(sale.order_line.mapped(
                    "amount_pending_invoicing_with_discount")))
