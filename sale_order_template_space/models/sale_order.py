# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_order_space_ids = fields.One2many(
        string="Sale Order Spaces",
        comodel_name="sale.order.space",
        inverse_name="sale_order_id",
        copy=True,
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {})
        sale = super().copy(default=default)
        if sale.sale_order_space_ids:
            sale.order_line.unlink()
        return sale
