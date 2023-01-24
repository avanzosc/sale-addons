# Copyright (c) 2023 Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    qty_available = fields.Float(
        string="RQ", compute="_compute_quantities",
        digits="Product Unit of Measure", compute_sudo=False)
    virtual_available = fields.Float(
        string="AQ", compute="_compute_quantities",
        digits="Product Unit of Measure", compute_sudo=False)

    @api.depends("product_id", "order_id", "order_id.warehouse_id")
    def _compute_quantities(self):
        for line in self:
            qty_available = 0
            virtual_available = 0
            if (line.product_id and line.order_id.warehouse_id and
                    line.order_id.warehouse_id.lot_stock_id):
                location = line.order_id.warehouse_id.lot_stock_id
                qty_available = line.product_id.with_context(
                    location=location.id).qty_available
                virtual_available = line.product_id.with_context(
                    location=location.id).virtual_available
            line.qty_available = qty_available
            line.virtual_available = virtual_available
