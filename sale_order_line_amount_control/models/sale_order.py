# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        for sale in self:
            min_price_unit = sale._get_min_price_unit()
            lines = sale.order_line.filtered(
                lambda x: x.price_unit == min_price_unit)
            if lines:
                raise UserError(
                    _('You have %s line(s) with an amount less than or equal '
                      'to %s') % (len(lines), min_price_unit))
        return super(SaleOrder, self).action_confirm()

    def _get_min_price_unit(self):
        return 1
