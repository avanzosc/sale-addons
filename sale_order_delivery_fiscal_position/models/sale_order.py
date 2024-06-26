# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("partner_shipping_id", "partner_id", "company_id")
    def onchange_partner_shipping_id(self):
        result = super(SaleOrder, self).onchange_partner_shipping_id()
        if (
            self.partner_shipping_id
            and self.partner_shipping_id.property_account_position_id
        ):
            self.fiscal_position_id = (
                self.partner_shipping_id.property_account_position_id.id
            )
        return result
