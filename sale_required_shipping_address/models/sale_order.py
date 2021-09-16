# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


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
                if len(deliveries) == 1:
                    self.partner_shipping_id = deliveries.id
                else:
                    if len(deliveries) > 1:
                        self.partner_shipping_id = False
            self.allowed_shipping_ids = [(6, 0, partners.ids)]
        return result

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        if not self.partner_id:
            return
        warning = super(SaleOrder, self).onchange_partner_id_warning()
        if warning is None:
            warning = {}
        my_warning = {} if warning == bool else warning
        if len(self.allowed_shipping_ids) > 1:
            message = _('More than one delivery address found ')
            if not my_warning:
                title = _("Warning for %s") % self.partner_id.name
                warning2 = {
                    'title': title,
                    'message': message,
                }
                my_warning = {'warning': warning2}
            else:
                origin_warning = my_warning.get('warning')
                origin_message = origin_warning.get('message')
                my_message = ('{}\n{}').format(origin_message, message)
                my_warning['warning']['message'] = my_message
        if my_warning:
            return my_warning
        else:
            return warning
