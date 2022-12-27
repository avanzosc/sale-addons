# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_packaging_id = fields.Many2one(
        compute=False, precompute=False)
    product_packaging_qty = fields.Float(
        compute=False, precompute=True)

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id and self.product_packaging_qty:
            self.product_uom_qty = (
                self.product_packaging_qty * self.product_packaging_id.qty)
        else:
            if self.product_packaging_id and self.product_uom_qty:
                newqty = self.product_packaging_id._check_qty(
                    self.product_uom_qty, self.product_uom, "UP")
                self.product_packaging_qty = newqty
                return super(
                    SaleOrderLine, self)._onchange_product_packaging_id()

    @api.onchange("product_packaging_qty")
    def _onchange_product_packaging_qty(self):
        if self.product_packaging_id and self.product_packaging_qty:
            self.product_uom_qty = (
                self.product_packaging_qty * self.product_packaging_id.qty)

    @api.onchange("product_uom_qty")
    def _onchange_product_uom_qty(self):
        if self.product_packaging_id and self.product_uom_qty:
            packaging_uom = self.product_packaging_id.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(
                self.product_uom_qty, packaging_uom)
            self.product_packaging_qty = float_round(
                packaging_uom_qty / self.product_packaging_id.qty,
                precision_rounding=packaging_uom.rounding)
