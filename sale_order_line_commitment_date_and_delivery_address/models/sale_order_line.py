from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(
        related="order_id.commitment_date",
        string="Commitment Date",
        store=True,
    )
    delivery_address = fields.Many2one(
        related="order_id.partner_shipping_id",
        string="Delivery Address",
        # store=True, Cannot be stored because it's a computed field
    )
