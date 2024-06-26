# Copyright 2021 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_delivery_line(self, carrier, price_unit):
        result = super(SaleOrder, self)._create_delivery_line(carrier, price_unit)
        if carrier.free_over and self.currency_id.is_zero(price_unit):
            result.name = carrier.with_context(lang=self.partner_id.lang).name
        return result
