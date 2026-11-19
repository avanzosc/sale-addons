from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_commitmen_date(self):
        if "default_commitment_date" in self.env.context:
            return self.env.context.get("default_commitment_date")
        else:
            return self.order_id.commitment_date

    commitment_date = fields.Datetime(default=_get_commitmen_date)
    delivery_address_id = fields.Many2one(
        "res.partner",
        related="order_id.partner_shipping_id",
        store=True,
    )
