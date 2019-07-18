# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        if self.company_id.autocreate_sale_analytic_account:
            for order in self.filtered(lambda o: not o.analytic_account_id):
                order._create_analytic_account()
        return res
