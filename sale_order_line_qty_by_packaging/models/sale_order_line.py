# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_packaging = fields.Many2one(
        domain="[('product_id','=',product_id)]"
    )
    product_packaging_qty = fields.Float(
        string="Packaging Q."
    )

    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_id and len(self.product_id.packaging_ids) == 1:
            self.product_packaging = self.product_id.packaging_ids[0].id
        return result

    @api.onchange("product_packaging")
    def _onchange_product_packaging(self):
        result = super(SaleOrderLine, self)._onchange_product_packaging()
        if self.product_packaging:
            self.product_packaging_qty = 1
            self.product_uom_qty = self.product_packaging.qty
        else:
            self.product_packaging_qty = 0
            self.product_uom_qty = 1
        return result

    @api.onchange("product_packaging_qty")
    def _onchange_product_packaging_qty(self):
        if self.product_packaging and self.product_packaging_qty:
            self.product_uom_qty = (
                self.product_packaging_qty * self.product_packaging.qty)

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        result = super(SaleOrderLine, self). product_uom_change()
        if self.product_packaging and self.product_uom_qty:
            packaging_uom = self.product_packaging.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(
                self.product_uom_qty, packaging_uom)
            self.product_packaging_qty = float_round(
                packaging_uom_qty / self.product_packaging.qty,
                precision_rounding=packaging_uom.rounding)
        return result

    @api.onchange("product_uom_qty")
    def _onchange_product_uom_qty(self):
        result = super(SaleOrderLine, self)._onchange_product_uom_qty()
        if self.product_packaging and self.product_uom_qty:
            packaging_uom = self.product_packaging.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(
                self.product_uom_qty, packaging_uom)
            self.product_packaging_qty = float_round(
                packaging_uom_qty / self.product_packaging.qty,
                precision_rounding=packaging_uom.rounding)
        return result
