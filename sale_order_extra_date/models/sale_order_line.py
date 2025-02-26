from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date1 = fields.Datetime(
        string="Customer Order Creation Date",
        help="Customer order creation date",
        related="order_id.date1",
        store=True,
    )
    date2 = fields.Datetime(
        string="Reconfirmed Date",
        help="Reconfirmed date",
    )
