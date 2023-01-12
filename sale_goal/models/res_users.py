# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    sale_partner_ids = fields.One2many(
        comodel_name="res.partner",
        inverse_name="user_id",
        string="Customers",
    )
    sale_partner_count = fields.Integer(
        compute="_compute_sale_partner_count",
        string="Customer Count",
    )
    commercial_sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="user_id",
        string="Sales",
    )
    sales_goal_monthly = fields.Float(
        string="Monthly Sales Goal",
        compute="_compute_sales_goal",
    )
    sales_goal_yearly = fields.Float(
        string="Yearly Sales Goal",
        compute="_compute_sales_goal",
    )
    current_month_sale_amount = fields.Float(
        compute="_compute_current_month_sale_amount",
        string="Current Month Sale Amount",
    )
    current_year_sale_amount = fields.Float(
        compute="_compute_current_year_sale_amount",
        string="Current Year Sale Amount",
    )

    def _compute_sale_partner_count(self):
        for record in self:
            record.sale_partner_count = len(record.sale_partner_ids)

    @api.depends(
        "sale_partner_ids",
        "sale_partner_ids.sales_goal_monthly",
        "sale_partner_ids.sales_goal_yearly",
    )
    def _compute_sales_goal(self):
        for record in self:
            partners = record.sale_partner_ids
            record.sales_goal_monthly = sum(partners.mapped("sales_goal_monthly"))
            record.sales_goal_yearly = sum(partners.mapped("sales_goal_yearly"))

    def _compute_current_month_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            sale_orders = record.commercial_sale_order_ids.filtered(
                lambda o: today.month == o.date_order.month
                and today.year == o.date_order.year
                and o.state not in ("draft", "sent", "cancel")
            )
            record.current_month_sale_amount = sum(
                sale_orders.mapped("order_line.price_subtotal")
            )

    def _compute_current_year_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            sale_orders = record.commercial_sale_order_ids.filtered(
                lambda o: today.year == o.date_order.year
                and o.state not in ("draft", "sent", "cancel")
            )
            record.current_year_sale_amount = sum(
                sale_orders.mapped("order_line.price_subtotal")
            )
