# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

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
        default=0.0,
    )
    current_year_sale_amount = fields.Float(
        default=0.0,
    )

    @api.onchange("sales_goal_monthly")
    def _onchange_sales_goal_monthly(self):
        self.sales_goal_yearly = self.sales_goal_monthly * 12

    @api.onchange("sales_goal_yearly")
    def _onchange_sales_goal_yearly(self):
        self.sales_goal_monthly = self.sales_goal_yearly / 12

    def _get_sale_amount(self, date_from, date_to):
        """Return sale amount by partner for the given date range."""
        sale_orders = self.env["sale.order"].search(
            [
                ("partner_id", "in", self.ids),
                ("state", "not in", ("draft", "sent", "cancel")),
                ("date_order", ">=", date_from),
                ("date_order", "<", date_to),
            ]
        )

        amounts = dict.fromkeys(self.ids, 0.0)

        for order in sale_orders:
            if order.partner_id.id in amounts:
                amounts[order.partner_id.id] += sum(
                    order.order_line.mapped("price_subtotal")
                )

        return amounts

    def calculate_current_month_sale_amount(self):
        today = fields.Date.context_today(self)
        date_from = today.replace(day=1)
        date_to = date_from + relativedelta(months=1)

        amounts = self._get_sale_amount(date_from, date_to)

        for partner in self:
            partner.current_month_sale_amount = amounts[partner.id]

    def calculate_current_year_sale_amount(self):
        today = fields.Date.context_today(self)
        date_from = today.replace(month=1, day=1)
        date_to = date_from + relativedelta(years=1)

        amounts = self._get_sale_amount(date_from, date_to)

        for partner in self:
            partner.current_year_sale_amount = amounts[partner.id]

    def process_current_sale_amount(self):
        partners = self.search([])

        partners.calculate_current_month_sale_amount()
        partners.calculate_current_year_sale_amount()
