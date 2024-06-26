# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_create_return_purchase_order(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("The sale order does not have the partner."))
        if not self.type_id:
            raise UserError(_("The sale order does not have the type."))
        if not self.type_id.picking_type_id:
            raise UserError(_("The sales order type does not have the picking type."))
        if self.type_id.picking_type_id.code != "outgoing":
            raise UserError(_("The picking type must be outgoing."))
        if not self.type_id.picking_type_id.return_picking_type_id:
            raise UserError(
                _("The picking type must have informed the return picking type.")
            )
        purchase = self.env["purchase.order"].create(
            {
                "partner_id": self.partner_id.id,
                "picking_type_id": (
                    self.type_id.picking_type_id.return_picking_type_id.id
                ),
                "is_devolution": True,
            }
        )
        purchase.action_return_returnable()
        return {
            "name": _("Return Purchase Order"),
            "view_mode": "form,tree",
            "res_model": "purchase.order",
            "res_id": purchase.id,
            "type": "ir.actions.act_window",
            "context": dict(self.env.context),
        }
