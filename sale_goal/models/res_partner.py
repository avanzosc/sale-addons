# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sales_goal_monthly = fields.Float(
        string="Monthly Sales Goal",
        default=0.0,
    )
    sales_goal_yearly = fields.Float(
        string="Yearly Sales Goal",
        default=0.0,
    )
    current_month_sale_amount = fields.Float(
        compute="_compute_current_month_sale_amount",
        string="Current Month Sale Amount",
        default=0.0,
    )
    current_year_sale_amount = fields.Float(
        compute="_compute_current_year_sale_amount",
        string="Current Year Sale Amount",
        default=0.0,
    )

    def _compute_current_month_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            sale_orders = record.sale_order_ids.filtered(
                lambda o: today.month == o.date_order.month and
                today.year == o.date_order.year and
                o.state not in ("draft", "sent", "cancel"))
            record.current_month_sale_amount = sum(
                sale_orders.mapped("order_line.price_subtotal"))

    def _compute_current_year_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            sale_orders = record.sale_order_ids.filtered(
                lambda o: today.year == o.date_order.year and
                o.state not in ("draft", "sent", "cancel"))
            record.current_year_sale_amount = sum(
                sale_orders.mapped("order_line.price_subtotal"))

    @api.onchange("sales_goal_monthly")
    def onchange_sales_goal_monthly(self):
        for record in self:
            record.sales_goal_yearly = record.sales_goal_monthly * 12

    @api.onchange("sales_goal_yearly")
    def onchange_sales_goal_yearly(self):
        for record in self:
            record.sales_goal_monthly = record.sales_goal_yearly / 12
