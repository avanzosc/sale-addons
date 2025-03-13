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

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        Overrides the default behavior when changing the partner
        on a sale order to keep the 'note' field unchanged.
        """
        original_note = self.note
        result = super(SaleOrder, self).onchange_partner_id()
        if original_note:
            self.note = original_note
        return result
