# Copyright 2023 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ResPartner(models.Model):
    _inherit = "res.partner"

    sales_goal_monthly = fields.Float(
        string="Monthly Sales Goal",
        digits=dp.get_precision("Product Price"),
    )
    sales_goal_yearly = fields.Float(
        string="Yearly Sales Goal",
        digits=dp.get_precision('Product Price'),
    )
    current_month_sale_amount = fields.Float()
    current_year_sale_amount = fields.Float()

    def _compute_current_month_sale_amount(self):
        for record in self:
            record.current_month_sale_amount = 0.0

    def _compute_current_year_sale_amount(self):
        for record in self:
            record.current_year_sale_amount = 0.0

    @api.onchange("sales_goal_monthly")
    def onchange_sales_goal_monthly(self):
        for record in self:
            record.sales_goal_yearly = record.sales_goal_monthly * 12

    @api.onchange("sales_goal_yearly")
    def onchange_sales_goal_yearly(self):
        for record in self:
            record.sales_goal_monthly = record.sales_goal_yearly / 12
