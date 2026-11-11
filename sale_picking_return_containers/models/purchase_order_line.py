# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    max_return = fields.Float(string="Max. Qty to Return")
    sale_order_line_ids = fields.Many2many(
        string="Sale Order Lines",
        comodel_name="sale.order.line",
        relation="rel_saleline_purchaseline",
        column1="sale_order_line_id",
        column2="purchase_order_line_id",
    )

    @api.constrains("max_return", "product_qty")
    def _check_max_return(self):
        for line in self:
            if (
                line.product_id.returnable
                and line.max_return != 0
                and (line.product_qty > line.max_return)
                and (line.price_unit != 0)
            ):
                raise ValidationError(
                    _(
                        "The quantity can't be bigger than the maximum "
                        + "quantity to return."
                    )
                )

    @api.onchange("product_qty", "price_unit")
    def _onchange_product_qty(self):
        if self.product_qty and self.sale_order_line_ids:
            self.price_unit = self.sale_order_line_ids[:1].price_unit
