# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleSintraAssign(models.TransientModel):
    _name = "sale.sintra.assign"
    _description = "Assign Sales Orders to a Sintra"

    sintra_id = fields.Many2one(
        comodel_name="sale.sintra", string="Sintra", required=True
    )
    sale_order_ids = fields.Many2many(
        comodel_name="sale.order", string="Sales Orders", readonly=True
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if (
            "sale_order_ids" in fields_list
            and self.env.context.get("active_model") == "sale.order"
        ):
            res["sale_order_ids"] = [
                fields.Command.set(self.env.context.get("active_ids", []))
            ]
        return res

    def action_assign(self):
        self.sale_order_ids.write({"sintra_id": self.sintra_id.id})
