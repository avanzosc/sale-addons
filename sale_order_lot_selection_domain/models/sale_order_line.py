# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_id")
    def onchange_lot_domain(self):
        self.ensure_one()
        result = False
        if self.product_id:
            lots = []
            lot = self.env["stock.production.lot"].search([
                ('product_id', '=', self.product_id.id),
                ("company_id", "=", self.company_id.id)])
            for line in lot:
                qty = line.product_qty
                if qty > 0:
                    lots.append(line.id)
            result = {"domain": {"lot_id": [('id', 'in', lots)]}}
        return result
