# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    pending_returns = fields.Boolean(compute='_compute_pending_pickings')
    pending_deliveries = fields.Boolean(compute='_compute_pending_pickings')
    
    @api.depends('picking_ids')
    def _compute_pending_pickings(self):
        for order in self:
            pending_returns = False
            pending_deliveries = False
    
            for picking in order.picking_ids:
                if picking.state not in ('done', 'cancel'):
                    if picking.picking_type_id.code == 'incoming':
                        pending_returns = True
                    elif picking.picking_type_id.code == 'outgoing':
                        pending_deliveries = True
    
                if pending_returns and pending_deliveries:
                    break
    
            order.pending_returns = pending_returns
            order.pending_deliveries = pending_deliveries

    def button_confirm_pickings(self):
        result = super(SaleOrder, self).button_confirm_pickings()
        for line in self.order_line:
            if (
                line.product_id
                and (line.product_id.tracking != "none")
                and not (line.lot_id)
                and line.return_qty
            ):
                raise ValidationError(
                    _("The product {} has not lot").format(line.product_id.name)
                )
        return result

    def button_return_picking(self):
        for order in self:
            return_pickings = order.picking_ids.filtered(
                lambda p: p.state not in ['done', 'cancel'] and p.picking_type_id.return_picking_type_id
            )
            if not return_pickings:
                raise ValidationError(_("No pending return delivery picking was found for this order."))
            else:
                result = super(SaleOrder, self).button_confirm_pickings()
        return result
