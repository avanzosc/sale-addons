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
        default=0.0,
        store=True,
    )
    sales_goal_yearly = fields.Float(
        string="Yearly Sales Goal",
        compute="_compute_sales_goal",
        default=0.0,
        store=True,
    )
    current_month_sale_amount = fields.Float(
        string="Current Month Sale Amount",
        default=0.0,
    )
    current_year_sale_amount = fields.Float(
        string="Current Year Sale Amount",
        default=0.0,
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

    def calculate_current_month_sale_amount(self):
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

    def calculate_current_year_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            sale_orders = record.commercial_sale_order_ids.filtered(
                lambda o: today.year == o.date_order.year
                and o.state not in ("draft", "sent", "cancel")
            )
            record.current_year_sale_amount = sum(
                sale_orders.mapped("order_line.price_subtotal")
            )

    def process_current_sale_amount(self):
        today = fields.Date.context_today(self)
        year_orders = self.env["sale.order"].search(
            [
                ("state", "not in", ["draft", "sent", "cancel"]),
                ("date_order", ">=", today.replace(month=1, day=1)),
                ("date_order", "<", today.replace(year=today.year + 1, month=1, day=1)),
            ]
        )
        users = self.search(
            [
                ("id", "not in", year_orders.mapped("user_id").ids),
            ]
        )
        users.write(
            {
                "current_year_sale_amount": 0.0,
                "current_month_sale_amount": 0.0,
            }
        )
        year_orders.mapped("user_id").calculate_current_year_sale_amount()
        month_orders = year_orders.filtered(lambda o: today.month == o.date_order.month)
        users = self.search(
            [
                ("id", "not in", month_orders.mapped("user_id").ids),
            ]
        )
        users.write(
            {
                "current_month_sale_amount": 0.0,
            }
        )
        month_orders.mapped("user_id").calculate_current_month_sale_amount()
