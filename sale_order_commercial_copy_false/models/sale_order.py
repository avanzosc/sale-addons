from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    user_id = fields.Many2one(
        "res.users",
        copy=False,
    )
