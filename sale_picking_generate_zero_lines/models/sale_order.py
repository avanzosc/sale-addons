# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    picking_count = fields.Integer(
        string="Picking Count", compute="_compute_picking_count", store=True
    )

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_picking_count(self):
        for sale in self:
            sale.picking_count = len(sale.picking_ids)

    def button_return_picking(self):
        self.ensure_one()
        if len(self.picking_ids) != 1 or self.picking_ids.state != "done":
            raise UserError(_("You can only return one done picking."))
        picking = self.picking_ids[0]
        wiz = self.env["stock.return.picking"].create(
            {
                "picking_id": picking.id,
            }
        )
        wiz._onchange_picking_id()
        return wiz.sudo().create_returns()
