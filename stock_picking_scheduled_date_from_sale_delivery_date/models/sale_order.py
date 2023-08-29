# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def write(self, vals):
        result = super(SaleOrder, self).write(vals)
        if "commitment_date" in vals:
            for sale in self:
                sale.picking_ids.write(
                    {"scheduled_date": vals.get("commitment_date")})
        return result
