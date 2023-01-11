# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sales_goal_yearly_percentage = fields.Float(
        'Yearly objective',
        compute="_compute_sales_goal_yearly_percentage",
        default=0.0,
        store=True,)
    sales_goal_monthly_percentage = fields.Float(
        'Monthly objective', 
        copmute="_compute_sales_goal_monthly_percentage",
        default=0.0,
        store=True,)

    @api.depends('order_partner_id', 'order_partner_id.sales_goal_monthly', 'price_subtotal')
    def _compute_sales_goal_monthly_percentage(self):
        for record in self:
            if record.order_partner_id.sales_goal_monthly:
                record.sales_goal_monthly_percentage = record.order_partner_id.price_subtotal * 100 / record.order_partner_id.sales_goal_monthly
            else:
                record.sales_goal_monthly_percentage = 0.0

    @api.depends('order_partner_id', 'order_partner_id.sales_goal_yearly', 'price_subtotal')
    def _compute_sales_goal_yearly_percentage(self):
        for record in self:
            if record.order_partner_id.sales_goal_yearly:
                record.sales_goal_yearly_percentage = record.order_partner_id.price_subtotal * 100 / record.order_partner_id.sales_goal_yearly
            else:
                record.sales_goal_yearly_percentage = 0.0
