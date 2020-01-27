# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sepa_count = fields.Integer(
        string="# SEPA", compute='_compute_sepa_count')

    @api.multi
    def _compute_sepa_count(self):
        for sale in self:
            sale.sepa_count = len(sale._find_payer_mandates())

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            lines = sale.mapped('order_line').filtered(lambda x: x.payer_ids)
            for line in lines:
                line._generate_sepa_mandate()
        return res

    @api.multi
    def action_view_sepa_from_sale_order(self):
        self.ensure_one()
        action = self.env.ref('account_banking_mandate.mandate_action')
        action_dict = action and action.read()[0]
        domain = expression.AND([
            [('id', 'in', self._find_payer_mandates().ids)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain})
        return action_dict

    @api.multi
    def _find_payer_mandates(self):
        self.ensure_one()
        mandates = self.env["account.banking.mandate"]
        for line in self.order_line:
            mandates |= line._find_payer_mandates()
        return mandates
