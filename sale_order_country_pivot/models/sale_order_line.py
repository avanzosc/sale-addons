from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    partner_country_id = fields.Many2one(
        related="order_id.partner_country_id",
        string="Country",
        store=True,
    )
    partner_state_id = fields.Many2one(
        related="order_id.partner_state_id",
        string="State",
        store=True,
    )
    fiscal_position_id = fields.Many2one(
        related="order_id.fiscal_position_id",
        string="Fiscal Position",
        store=True,
    )
