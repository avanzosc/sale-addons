# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrderImport(models.Model):
    _inherit = "sale.order.import"

    type_id = fields.Many2one(
        string="Sale Order Type",
        comodel_name="sale.order.type",
        copy=False,
    )

    @api.onchange("warehouse_id")
    def _onchange_warehouse_id_type(self):
        self.type_id = False
        if self.warehouse_id:
            types = self.env["sale.order.type"].search(
                [("warehouse_id", "=", self.warehouse_id.id)]
            )
            if len(types) == 1:
                self.type_id = types
