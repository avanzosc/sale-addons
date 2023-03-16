# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_id, name, origin, company_id, values):
        values = super(StockRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin,
            company_id, values)
        if "sale_line_id" in values and values.get("sale_line_id", False):
            sale_line = self.env["sale.order.line"].browse(
                values.get("sale_line_id"))
            if (sale_line.order_id.type_id and
                    sale_line.order_id.type_id.picking_type_id):
                values['picking_type_id'] = (
                    sale_line.order_id.type_id.picking_type_id.id)
                values['location_id'] = (
                    sale_line.order_id.type_id.picking_type_id.default_location_src_id.id)
                values['location_dest_id'] = (
                    sale_line.order_id.type_id.picking_type_id.default_location_dest_id.id)
                if sale_line.order_id.type_id.picking_type_id.sequence_id:
                    values['sequence'] = sale_line.order_id.type_id.picking_type_id.sequence_id.id
        return values
