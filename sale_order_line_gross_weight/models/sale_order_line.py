# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    gross_weight = fields.Float(
        string="Gross Field")

    @api.onchange("gross_weight")
    def _onchange_gross_weight(self):
        if self.product_packaging and self.gross_weight:
            weight_categ = self.env.ref('uom.product_uom_categ_kgm')
            product_uom_qty = self.gross_weight
            if self.product_packaging and self.product_packaging.weight and self.product_packaging_qty and self.product_uom.category_id == weight_categ:
                product_uom_qty -= self.product_packaging.weight * self.product_packaging_qty
            if self.palet_id and self.palet_id.weight and self.palet_qty and self.product_uom.category_id == weight_categ:
                product_uom_qty -= self.palet_id.weight * self.palet_qty
            self.product_uom_qty = product_uom_qty

    @api.onchange("product_uom_qty")
    def _onchange_product_uom_qty(self):
        return False
