# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_route_ids = fields.Many2many(
        comodel_name="stock.location.route",
        column1="line_id",
        column2="route_id",
        relation="rel_stock_route_sale_line",
        related="product_id.route_ids",
        string="Routes",
    )
