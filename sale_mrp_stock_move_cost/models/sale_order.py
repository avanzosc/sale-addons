# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    production_ids = fields.One2many(
        string="Manufacturing orders", comodel_name="mrp.production",
        inverse_name="sale_id", copy=False
    )
    manufacturing_order_cost = fields.Float(
        string="Mo's Cost", digits="Product Price", copy=False, store=True,
        compute="_compute_manufacturing_order_cost"
    )
    sale_margin_with_manufacturing_order = fields.Float(
        string="Sale margin with Mo's", digits="Product Price", copy=False,
        store=True, compute="_compute_manufacturing_order_cost")

    @api.depends("amount_untaxed", "production_ids", "production_ids.cost")
    def _compute_manufacturing_order_cost(self):
        for sale in self:
            manufacturing_order_cost = 0
            sale_margin = 0
            if sale.production_ids:
                manufacturing_order_cost = sum(
                    sale.production_ids.mapped("cost"))
            if manufacturing_order_cost > 0:
                sale_margin = sale.amount_untaxed - manufacturing_order_cost
            sale.manufacturing_order_cost = manufacturing_order_cost
            sale.sale_margin_with_manufacturing_order = sale_margin
