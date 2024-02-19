# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_invoice_id")
    def _onchange_partner_invoice_id(self):
        self = self.with_company(self.company_id)
        values = {
            "payment_term_id": self.partner_invoice_id.property_payment_term_id
            and self.partner_invoice_id.property_payment_term_id.id
            or self.payment_term_id.id,
        }
        self.update(values)

    @api.depends("partner_id", "partner_invoice_id")
    def _compute_payment_mode(self):
        for order in self:
            if order.partner_invoice_id.customer_payment_mode_id:
                order.payment_mode_id = (
                    order.partner_invoice_id.customer_payment_mode_id
                )
            else:
                super()._compute_payment_mode()
