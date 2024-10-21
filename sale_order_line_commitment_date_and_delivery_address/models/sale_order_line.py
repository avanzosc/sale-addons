from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    commitment_date = fields.Datetime(
        related="order_id.commitment_date",
        string="Commitment Date",
        store=True,
    )
    delivery_address = fields.Many2one(
        "res.partner",
        compute="_compute_delivery_address",
        store=True,
    )

    def _compute_delivery_address(self):
        for line in self:
            if line.order_id and line.order_id.partner_shipping_id:
                line.delivery_address = line.order_id.partner_shipping_id.id
            else:
                line.delivery_address = False
