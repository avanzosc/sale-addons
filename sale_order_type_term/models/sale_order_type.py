# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    description = fields.Text(string="Terms and Conditions")
