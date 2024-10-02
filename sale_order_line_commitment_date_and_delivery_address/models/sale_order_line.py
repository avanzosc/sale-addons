from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Date(
        related="order_id.commitment_date",
        string="Commitment Date",
        store=True,
    )
    delivery_address = fields.Char(
        related="order_id.partner_id.contact_address",
        string="Delivery Address",
        store=True,
    )
