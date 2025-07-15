# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    package_qty = fields.Integer(string="Packages")
    product_packaging = fields.Many2one(
        string="Packaging",
        comodel_name="product.packaging",
    )

    @api.onchange("package_qty", "product_packaging", "product_packaging.qty")
    def onchange_product_packaging(self):
        self.ensure_one()
        if self.package_qty:
            self.qty_done = self.product_packaging.qty * self.package_qty

    @api.onchange("move_id")
    def onchange_move_id(self):
        self.ensure_one()
        super().onchange_move_id()
        if self.move_id:
            self.package_qty = self.move_id.package_qty
            self.product_packaging = self.move_id.product_packaging
