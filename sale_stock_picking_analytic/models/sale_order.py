# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super().action_confirm()
        for sale in self.filtered(lambda x: x.analytic_account_id):
            pickings = sale.picking_ids.filtered(lambda z: not z.analytic_account_id)
            if pickings:
                pickings.write({"analytic_account_id": sale.analytic_account_id})
        return result

    def put_analytic_in_out_picking_from_sale(self):
        sales = self.filtered(
            lambda x: x.analytic_account_id and x.state not in ("draft", "cancel")
        )
        for sale in sales:
            pickings = sale.picking_ids.filtered(
                lambda z: not z.analytic_account_id and z.state == "done"
            )
            if pickings:
                pickings.write({"analytic_account_id": sale.analytic_account_id})
