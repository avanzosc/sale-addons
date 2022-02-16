# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange("product_uom_qty")
    def onchange_amount_commission(self):
        if self.product_uom_qty:
            self.agent_ids.object_id.product_uom_qty = self.product_uom_qty
