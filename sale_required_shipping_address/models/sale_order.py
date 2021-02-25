# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allowed_shipping_ids = fields.Many2many(
        string='Allowed shipping', comodel_name='res.partner')

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            partners = self.partner_id
            if self.partner_id.child_ids:
                deliveries = self.partner_id.child_ids.filtered(
                    lambda x: x.type == 'delivery')
                for delivery in deliveries:
                    partners += delivery
                if len(deliveries) > 1:
                    self.partner_shipping_id = False
            self.allowed_shipping_ids = [(6, 0, partners.ids)]
        return result
