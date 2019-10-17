# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self.filtered(lambda c: c.analytic_account_id):
            sale.mapped('picking_ids').write({
                'analytic_account_id': sale.analytic_account_id.id,
            })
        return res
