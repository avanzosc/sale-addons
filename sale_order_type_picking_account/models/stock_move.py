# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_new_picking_values(self):
        values = super(StockMove, self)._get_new_picking_values()
        group = self.mapped("group_id")
        if group and group.sale_id and group.sale_id.type_id:
            values["sale_type_id"] = group.sale_id.type_id.id
        return values
