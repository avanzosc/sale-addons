# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        return_lines = order.order_line.filtered(
            lambda l: l.return_qty and l.return_qty > 0
        )
        if return_lines:
            for line in return_lines:
                line._create_and_update_return()
        return order

    def button_validate_everything(self):
        for order in self:
            if order.state in ["draft", "sent"]:
                order.action_confirm()
            pickings = order.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            )
            if not pickings:
                raise ValidationError(
                    _("There are no pending pickings to process for this order.")
                )
            for picking in pickings:
                picking.action_confirm()
                action = picking.button_validate()
                if isinstance(action, dict):
                    return action
        return True
