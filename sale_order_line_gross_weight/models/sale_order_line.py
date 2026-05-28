# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    gross_weight = fields.Float(string="Gross Field")

    def _get_packaging_weight(self):
        self.ensure_one()
        packaging = self.product_packaging_id
        if not packaging:
            return 0.0
        if "weight" in packaging._fields and packaging.weight:
            return packaging.weight
        if packaging.package_type_id and packaging.package_type_id.base_weight:
            return packaging.package_type_id.base_weight
        return 0.0

    def _get_palet_weight(self):
        self.ensure_one()
        palet = self.palet_id
        if not palet:
            return 0.0
        if "weight" in palet._fields and palet.weight:
            return palet.weight
        if "base_weight" in palet._fields and palet.base_weight:
            return palet.base_weight
        return 0.0

    @api.onchange("gross_weight")
    def _onchange_gross_weight(self):
        if self.product_packaging_id and self.gross_weight:
            weight_categ = self.env.ref("uom.product_uom_categ_kgm")
            product_uom_qty = self.gross_weight
            packaging_weight = self._get_packaging_weight()
            if (
                self.product_packaging_id
                and packaging_weight
                and self.product_packaging_qty
                and self.product_uom.category_id == weight_categ
            ):
                product_uom_qty -= packaging_weight * self.product_packaging_qty
            palet_weight = self._get_palet_weight()
            if (
                self.palet_id
                and palet_weight
                and self.palet_qty
                and self.product_uom.category_id == weight_categ
            ):
                product_uom_qty -= palet_weight * self.palet_qty
            self.product_uom_qty = product_uom_qty

    @api.onchange("product_uom_qty")
    def _onchange_product_uom_qty(self):
        return False
