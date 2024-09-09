from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    salesman_id = fields.Many2one(
        "res.users",
        copy=False,
    )
