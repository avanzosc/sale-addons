# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        for sale in self.filtered(lambda x: x.analytic_account_id):
            pickings = sale.picking_ids.filtered(
                lambda z: not z.analytic_account_id)
            if pickings:
                pickings.write(
                    {'analytic_account_id': sale.analytic_account_id})
        return result
