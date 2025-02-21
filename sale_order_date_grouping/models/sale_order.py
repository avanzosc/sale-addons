# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_month = fields.Char(
        string="Sale Month",
        compute="_compute_date_fields",
        store=True,
    )
    sale_year = fields.Char(
        string="Sale Year",
        compute="_compute_date_fields",
        store=True,
    )
    sale_quarter = fields.Char(
        string="Sale Quarter",
        compute="_compute_date_fields",
        store=True,
    )

    @api.depends("confirmation_date")
    def _compute_date_fields(self):
        for record in self:
            if record.confirmation_date:
                month_number = record.confirmation_date.strftime("%m")
                month_name = record.confirmation_date.strftime("%B")
                record.sale_month = f"{month_number} {month_name}"
                record.sale_year = record.confirmation_date.strftime("%Y")
                record.sale_quarter = "Q" + str(
                    (record.confirmation_date.month - 1) // 3 + 1
                )
                print ('*** record.sale_year: ' + str(record.sale_year))
