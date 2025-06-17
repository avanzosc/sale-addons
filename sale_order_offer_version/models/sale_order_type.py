from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    is_offer_type = fields.Boolean(
        default=False,
    )
