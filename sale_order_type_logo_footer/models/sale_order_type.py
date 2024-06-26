# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    logo_for_reports = fields.Binary("Logo for reports")
    footer_for_reports = fields.Text("Footer for reports", translate=True)
