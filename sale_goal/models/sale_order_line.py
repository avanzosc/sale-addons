# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sales_goal_yearly_percentage = fields.Float(
        string="Yearly Goal Percentage",
        compute="_compute_sales_goal_percentage",
        store=True,
    )
    sales_goal_monthly_percentage = fields.Float(
        string="Monthly Goal Percentage",
        compute="_compute_sales_goal_percentage",
        store=True,
    )

    @api.depends(
        "order_partner_id.sales_goal_monthly",
        "order_partner_id.sales_goal_yearly",
        "price_subtotal",
    )
    def _compute_sales_goal_percentage(self):
        for line in self:
            monthly_goal = line.order_partner_id.sales_goal_monthly
            yearly_goal = line.order_partner_id.sales_goal_yearly

            line.sales_goal_monthly_percentage = (
                line.price_subtotal * 100.0 / monthly_goal if monthly_goal else 0.0
            )

            line.sales_goal_yearly_percentage = (
                line.price_subtotal * 100.0 / yearly_goal if yearly_goal else 0.0
            )
