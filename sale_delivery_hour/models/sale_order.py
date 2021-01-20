# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_hours = fields.Char(string="Delivery Hours")

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        if not self.partner_id:
            self.update({
                'delivery_hours': False,
            })
            return
        self.delivery_hours = self.partner_id.delivery_hours
