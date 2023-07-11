# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super(StockPicking, self).button_validate()
        for picking in self:
            if picking.sale_id and (
                picking.sale_id.auto_purchase_order_id) and (
                    picking.state == "done"):
                for moveline in picking.move_line_ids_without_package:
                    if moveline.product_packaging_id:
                        purchase_picking = picking.sale_id.sudo(
                            ).auto_purchase_order_id.picking_ids.filtered(
                        lambda c: c.state not in ('cancel', 'done'))[:1]
                        if purchase_picking:
                            purchase_line = purchase_picking.move_line_ids_without_package.filtered(lambda c: c.product_id == moveline.product_id and c.lot_id.name == moveline.lot_id.name)
                            if not purchase_line:
                                purchase_line = purchase_picking.move_line_ids_without_package.filtered(lambda c: c.product_id == moveline.product_id and not c.lot_id)
                            if purchase_line:
                                purchase_line.product_packaging_id = moveline.product_packaging_id.id
                                purchase_line.product_packaging_qty = moveline.product_packaging_qty
        return result
