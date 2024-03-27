# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    not_route_type = fields.Boolean(
        string="Not Route Type",
        related="type_id.not_route_type",
        store=True,
    )
    deliverement_menu = fields.Boolean(
        string="Deliverement Menu",
        compute="compute_deliverement_menu")

    def compute_deliverement_menu(self):
        for sale in self:
            deliverement = False
            if "default_deliverement_menu" in self.env.context and (
                self.env.context["default_deliverement_menu"]
            ):
                deliverement = True
            sale.deliverement_menu = deliverement
