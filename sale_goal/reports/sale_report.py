# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    sales_goal_yearly_percentage = fields.Float(
        string="Yearly Goal Percentage",
        readonly=True,
    )

    sales_goal_monthly_percentage = fields.Float(
        string="Monthly Goal Percentage",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()

        res.update(
            {
                "sales_goal_monthly_percentage": "l.sales_goal_monthly_percentage",
                "sales_goal_yearly_percentage": "l.sales_goal_yearly_percentage",
            }
        )

        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()

        res += """
            ,
            l.sales_goal_monthly_percentage,
            l.sales_goal_yearly_percentage
        """

        return res
