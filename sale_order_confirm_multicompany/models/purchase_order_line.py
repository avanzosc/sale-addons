# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    no_create_picking = fields.Boolean(default=False)

    def _create_or_update_picking(self):
        for line in self:
            if not line.no_create_picking:
                return super()._create_or_update_picking()
            else:
                line.no_create_picking = False
