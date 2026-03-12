# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_purchase_order_data(self, *args, **kwargs):
        values = super()._prepare_purchase_order_data(*args, **kwargs)
        if self.origin:
            values["origin"] = self.origin
        return values
