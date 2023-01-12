# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'
    
    sales_goal_yearly_percentage = fields.Float(
        string='Yearly objective', readonly=True)
    sales_goal_monthly_percentage = fields.Float(
        string='Monthly objective', readonly=True)

    def _query(self, with_clause='', fields=None, groupby='', from_clause=''):
        if not fields:
            fields = {}
        fields["sales_goal_monthly_percentage"] = ', l.sales_goal_monthly_percentage as sales_goal_monthly_percentage'
        fields["sales_goal_yearly_percentage"] = ', l.sales_goal_yearly_percentage as sales_goal_yearly_percentage'
        groupby += ', l.sales_goal_monthly_percentage, l.sales_goal_yearly_percentage'
        return super(SaleReport, self)._query(
            with_clause=with_clause, fields=fields, groupby=groupby,
            from_clause=from_clause)
