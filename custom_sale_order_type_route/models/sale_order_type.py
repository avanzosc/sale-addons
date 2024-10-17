# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    not_route_type = fields.Boolean(
        string="Not Route Type",
        default=False,
    )
    burden_picking_type = fields.Many2one(
        string="Burden Picking Type", comodel_name="stock.picking.type"
    )

    def action_view_contact(self):
        context = self.env.context.copy()
        context.update(
            {
                "default_sale_type": self.id,
            }
        )
        return {
            "name": _("Contacts"),
            "view_mode": "tree",
            "view_id": self.env.ref(
                "custom_sale_order_type_route.view_partner_tree_editable"
            ).id,
            "res_model": "res.partner",
            "domain": [("sale_type", "=", self.id)],
            "type": "ir.actions.act_window",
            "context": context,
        }
