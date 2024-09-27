# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        if "sale_blanker_order_date" in self.env.context:
            for i in range(len(vals_list) - 1, -1, -1):
                if "commitment_date" not in vals_list[i]:
                    del vals_list[i]
        if "sale_blanker_order_date" in self.env.context and not vals_list:
            return self.env["sale.order.line"]
        return super().create(vals_list)
