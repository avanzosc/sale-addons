# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("partner_id", "partner_invoice_id")
    def _compute_payment_mode(self):
        super()._compute_payment_mode()
        for order in self.filtered(
            lambda sale: sale.partner_invoice_id
            and sale.partner_invoice_id.customer_payment_mode_id
        ):
            order.payment_mode_id = order.partner_invoice_id.customer_payment_mode_id
