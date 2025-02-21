from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    date1 = fields.Datetime(
        string="Customer Order Creation Date",
        help="Customer order creation date",
    )
