# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    package_qty = fields.Integer(string="Packages")
    container = fields.Integer(string="Container")
    product_packaging = fields.Many2one(string="Packaging")

    @api.onchange("product_id")
    def _onchange_product(self):
        self.product_packaging = False
        if self.product_id and self.product_id.packaging_ids:
            self.product_packaging = self.product_id.packaging_ids[:1].id

    @api.onchange("package_qty", "product_packaging", "product_packaging.qty")
    def onchange_product_packaging(self):
        self.ensure_one()
        if self.package_qty:
            self.product_uom_qty = self.product_packaging.qty * self.package_qty

    def _check_package(self):
        result = super(SaleOrderLine, self)._check_package()
        if "warning" in result:
            result = {}
        return result
