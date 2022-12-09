# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    package_qty = fields.Integer(
        string="Packages",
        related="sale_line_id.package_qty",
        store=True)
    container = fields.Integer(
        string="Container",
        related="sale_line_id.container",
        store=True)
    product_packaging = fields.Many2one(
        string="Packaging",
        comodel_name="product.packaging",
        related="sale_line_id.product_packaging",
        store=True)

    @api.onchange("sale_line_id")
    def onchange_sale_line_id(self):
        self.ensure_one()
        if self.sale_line_id:
            self.product_packaging = self.sale_line_id.product_packaging.id
            self.package_qty = self.sale_line_id.package_qty
            self.container = self.sale_line_id.container
