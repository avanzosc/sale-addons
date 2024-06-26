# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange("type_id")
    def onchange_type_id(self):
        result = super(SaleOrder, self).onchange_type_id()
        for order in self.filtered(lambda x: x.type_id and x.type_id.description):
            order.note = order.type_id.description
        return result
