# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def button_return_picking(self):
        picking_act = super(SaleOrder, self).button_return_picking()
        picking = self.env["stock.picking"].browse(picking_act.get("res_id"))
        if len(picking) == 1:
            for line in picking.move_line_ids_without_package:
                if line.move_id.sale_line_id:
                    line.qty_done = line.move_id.sale_line_id.return_qty
            if not any([line.return_qty != 0 for line in self.order_line]):
                return picking_act
            else:
                picking.action_confirm()
                return picking.button_validate()
