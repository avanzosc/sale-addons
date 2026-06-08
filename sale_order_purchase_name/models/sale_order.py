# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    purchase_name = fields.Char(
        string="Purchase Orders", compute="_compute_purchase_name", compute_sudo=True
    )

    def _compute_purchase_name(self):
        for sale in self:
            purchases = sale._get_purchase_orders()
            sale.purchase_name = (
                ", ".join(purchases.mapped("name")) if purchases else ""
            )
