# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    picking_count = fields.Integer(
        string="Picking Count",
        compute="_compute_picking_count",
        store=True
    )

    @api.depends("picking_ids", "picking_ids.state")
    def _compute_picking_count(self):
        for sale in self:
            sale.picking_count = len(sale.picking_ids)

    def button_return_picking(self):
        for sale in self:
            if sale.picking_ids and len(sale.picking_ids) == 1 and sale.picking_ids[:1].state == "done":
                wiz_obj = self.env['stock.return.picking']
                vals = {'picking_id': sale.picking_ids[:1].id}
                wiz = wiz_obj.create(vals)
                wiz._onchange_picking_id()
                result = wiz.sudo().create_returns()
                return result
            else:
                raise UserError(_("You can only return one done picking."))
