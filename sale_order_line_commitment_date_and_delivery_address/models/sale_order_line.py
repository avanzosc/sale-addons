from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(
        related="order_id.commitment_date",
        string="Commitment Date",
        store=True,
    )
    delivery_address_id = fields.Many2one(
        "res.partner",
        related="order_id.partner_shipping_id",
        store=True,
    )
