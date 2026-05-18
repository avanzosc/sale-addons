# Copyright 2026 Eñaut Alberdi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    shipping_final_customer = fields.Boolean(
        string="Ship to final customer",
        default=False,
        help="Filters shipping addresses according to the final customer flag.",
    )

    @api.onchange("partner_id", "company_id", "shipping_final_customer")
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if self.partner_id:
            partners = self.partner_id.commercial_partner_id
            if partners.child_ids:
                deliveries = partners.child_ids.filtered(
                    lambda x: x.type == "delivery"
                    and x.final_customer == self.shipping_final_customer
                )
                for delivery in deliveries:
                    partners += delivery
                if len(deliveries) == 1:
                    self.partner_shipping_id = deliveries.id
                else:
                    if len(deliveries) > 1:
                        self.partner_shipping_id = False
            self.allowed_shipping_ids = [(6, 0, partners.ids)]
        return result
