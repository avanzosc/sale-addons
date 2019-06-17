# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self.filtered(lambda c: not c.analytic_account_id):
            account = self.env['account.analytic.account'].create(
                sale._catch_vals_for_analytic())
            sale.analytic_account_id = account.id
        for sale in self.filtered(lambda c: c.analytic_account_id):
            for picking in sale.mapped('picking_ids').filtered(
                    lambda x: not x.analytic_account_id):
                picking.analytic_account_id = sale.analytic_account_id.id
        return res

    def _catch_vals_for_analytic(self):
        vals = {'name': self.name,
                'partner_id': self.partner_id.id}
        return vals
