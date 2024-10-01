# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    not_route_type = fields.Boolean(
        string="Not Route Type",
        related="type_id.not_route_type",
        store=True,
    )
    deliverement_menu = fields.Boolean(
        string="Deliverement Menu", compute="_compute_deliverement_menu"
    )
    special_burden = fields.Boolean(
        string="Special Burden",
        default=False,
    )
    partner_distribution_sequence = fields.Integer(
        string="Partner Distribution Sequence",
        related="partner_shipping_id.distribution_sequence",
        store=True,
    )

    def _compute_deliverement_menu(self):
        for sale in self:
            deliverement = False
            if "default_deliverement_menu" in self.env.context and (
                self.env.context["default_deliverement_menu"]
            ):
                deliverement = True
            sale.deliverement_menu = deliverement

    @api.onchange("partner_id")
    def onchange_type_domain(self):
        result = {"domain": {"type_id": []}}
        if (
            self.partner_id
            and "default_deliverement_menu" in (self.env.context)
            and self.env.context["default_deliverement_menu"]
        ):
            types = self.env["sale.order.type"].search(
                [
                    ("not_route_type", "=", False),
                    ("company_id", "=", self.company_id.id),
                ]
            )
            result = {"domain": {"type_id": [("id", "in", types.ids)]}}
        return result

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.special_burden = self.partner_id.special_burden
        return result
