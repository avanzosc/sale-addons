# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_packaging_id = fields.Many2one(
        comodel_name='product.packaging',
        string="Packaging",
        domain="[('product_id','=',product_id)]",
        check_company=True)
    product_packaging_qty = fields.Float(
        string="Packaging Quantity")

    @api.onchange("product_id")
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        if self.product_id and len(self.product_id.packaging_ids) == 1:
            self.product_packaging_id = self.product_id.packaging_ids[0].id
        return result

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id:
            self.product_packaging_qty = 1
            self.product_uom_qty = self.product_packaging_id.qty
        else:
            self.product_packaging_qty = 0
            self.product_uom_qty = 1

    @api.onchange("product_packaging_qty")
    def _onchange_product_packaging_qty(self):
        if self.product_packaging_id and self.product_packaging_qty:
            self.product_uom_qty = (
                self.product_packaging_qty * self.product_packaging_id.qty)

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        result = super(SaleOrderLine, self).product_uom_change()
        if self.product_packaging_id and self.product_uom_qty:
            packaging_uom = self.product_packaging_id.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(
                self.product_uom_qty, packaging_uom)
            self.product_packaging_qty = float_round(
                packaging_uom_qty / self.product_packaging_id.qty,
                precision_rounding=packaging_uom.rounding)
        return result