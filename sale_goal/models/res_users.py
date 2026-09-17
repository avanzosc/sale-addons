# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

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
        compute_sudo=True,
        store=True,
    )
    sales_goal_yearly = fields.Float(
        string="Yearly Sales Goal",
        compute="_compute_sales_goal",
        compute_sudo=True,
        store=True,
    )
    current_month_sale_amount = fields.Float(
        default=0.0,
    )
    current_year_sale_amount = fields.Float(
        default=0.0,
    )

    @api.depends("sale_partner_ids")
    def _compute_sale_partner_count(self):
        for user in self:
            user.sale_partner_count = len(user.sale_partner_ids)

    @api.depends(
        "sale_partner_ids.sales_goal_monthly",
        "sale_partner_ids.sales_goal_yearly",
    )
    def _compute_sales_goal(self):
        for user in self:
            user.sales_goal_monthly = sum(
                user.sale_partner_ids.mapped("sales_goal_monthly")
            )
            user.sales_goal_yearly = sum(
                user.sale_partner_ids.mapped("sales_goal_yearly")
            )

    def _get_sale_amount(self, date_from, date_to):
        """Return sale amount by salesperson for the given date range."""
        sale_orders = self.env["sale.order"].search(
            [
                ("user_id", "in", self.ids),
                ("state", "not in", ("draft", "sent", "cancel")),
                ("date_order", ">=", date_from),
                ("date_order", "<", date_to),
            ]
        )

        amounts = dict.fromkeys(self.ids, 0.0)

        for order in sale_orders:
            if order.user_id.id in amounts:
                amounts[order.user_id.id] += sum(
                    order.order_line.mapped("price_subtotal")
                )

        return amounts

    def calculate_current_month_sale_amount(self):
        today = fields.Date.context_today(self)

        date_from = today.replace(day=1)
        date_to = date_from + relativedelta(months=1)

        amounts = self._get_sale_amount(date_from, date_to)

        for user in self:
            user.current_month_sale_amount = amounts[user.id]

    def calculate_current_year_sale_amount(self):
        today = fields.Date.context_today(self)

        date_from = today.replace(month=1, day=1)
        date_to = date_from + relativedelta(years=1)

        amounts = self._get_sale_amount(date_from, date_to)

        for user in self:
            user.current_year_sale_amount = amounts[user.id]

    def process_current_sale_amount(self):
        users = self.search([])

        users.calculate_current_month_sale_amount()
        users.calculate_current_year_sale_amount()
