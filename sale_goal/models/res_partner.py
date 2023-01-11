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
        string="Current Month Sale Amount",
        default=0.0,
    )
    current_year_sale_amount = fields.Float(
        string="Current Year Sale Amount",
        default=0.0,
    )

    @api.onchange("sales_goal_monthly")
    def onchange_sales_goal_monthly(self):
        for record in self:
            record.sales_goal_yearly = record.sales_goal_monthly * 12

    @api.onchange("sales_goal_yearly")
    def onchange_sales_goal_yearly(self):
        for record in self:
            record.sales_goal_monthly = record.sales_goal_yearly / 12

    def calculate_current_month_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            month_orders = record.sale_order_ids.filtered(
                lambda o: today.year == o.date_order.year
                and today.month == o.date_order.month
                and o.state not in ("draft", "sent", "cancel")
            )
            record.write(
                {
                    "current_month_sale_amount": sum(
                        month_orders.mapped("order_line.price_subtotal")
                    ),
                }
            )

    def calculate_current_year_sale_amount(self):
        today = fields.Date.context_today(self)
        for record in self:
            year_orders = record.sale_order_ids.filtered(
                lambda o: today.year == o.date_order.year
                and o.state not in ("draft", "sent", "cancel")
            )
            if year_orders:
                record.write(
                    {
                        "current_year_sale_amount": sum(
                            year_orders.mapped("order_line.price_subtotal")
                        ),
                    }
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
        partners = self.search(
            [
                ("id", "not in", year_orders.mapped("partner_id").ids),
                ("current_year_sale_amount", "!=", 0.0),
            ]
        )
        partners.write(
            {
                "current_year_sale_amount": 0.0,
                "current_month_sale_amount": 0.0,
            }
        )
        year_orders.mapped("partner_id").calculate_current_year_sale_amount()
        month_orders = year_orders.filtered(lambda o: today.month == o.date_order.month)
        partners = self.search(
            [
                ("id", "not in", month_orders.mapped("partner_id").ids),
                ("current_month_sale_amount", "!=", 0.0),
            ]
        )
        partners.write(
            {
                "current_month_sale_amount": 0.0,
            }
        )
        month_orders.mapped("partner_id").calculate_current_month_sale_amount()
