# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    returned_amount = fields.Float(string="Returned Amount")
    pending_qty = fields.Float(string="Pending Qty")

    @api.onchange("returned_amount", "qty_delivered")
    def onchange_pending_qty(self):
        if self.returned_amount or self.qty_delivered:
            self.pending_qty = self.qty_delivered - self.returned_amount

    @api.constrains("price_unit", "pending_qty")
    def _check_pending_qty(self):
        for line in self:
            if line.pending_qty < 0 and line.price_unit != 0:
                raise ValidationError(
                    _(
                        "The pending quantity negative only can be if "
                        + "the price unit is 0."
                    )
                )
