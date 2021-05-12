# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    contract_ids = fields.Many2many(
        string='Contracts', comodel_name='contract.contract',
        compute='_compute_contract_ids', store=True)
    count_contracts = fields.Integer(
        string='# Contracts', compute='_compute_count_contracts')
    contract_created = fields.Boolean(
        string='Contract created', default=False)
    contract_created_literal = fields.Char(
        string='Contract created literal')

    @api.multi
    @api.depends('order_line', 'order_line.contract_line_id')
    def _compute_contract_ids(self):
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.contract_line_id)
            contracts = lines.mapped('contract_line_id.contract_id')
            if contracts:
                sale.contract_ids = [(6, 0, contracts.ids)]

    @api.multi
    def _compute_count_contracts(self):
        for sale in self:
            sale.count_contracts = len(sale.contract_ids)

    @api.multi
    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        for sale in self:
            lines = sale.catch_lines_to_try()
            if lines:
                sale.create_contract_lines(lines)
                if sale.contract_created:
                    sale.contract_created_literal = _(
                        'A NEW CONTRACT HAS BEEN CREATED.')
                else:
                    sale.contract_created_literal = _(
                        'A NEW LINE(S) HAS BEEN CREATED IN AN EXISTING '
                        'CONTRACT.')
        return res

    def catch_lines_to_try(self):
        lines = self.order_line.filtered(
            lambda x: x.product_id and
            x.product_id.recurring_interval)
        return lines

    def create_contract_lines(self, lines):
        cond = [('partner_id', '=', self.partner_id.id),
                ('contract_type', '=', 'sale'),
                '|', ('date_end', '=', False),
                ('date_end', '>', fields.Date.context_today(self))]
        contract = self.env['contract.contract'].search(cond, limit=1)
        if not contract:
            contract = self.create_contract()
            contract._onchange_partner_id()
            contract.journal_id = contract._default_journal().id
        for line in lines:
            line.contract_line_id = line._create_contract_line(contract).id

    def create_contract(self):
        vals = self._catch_values_for_create_contract()
        self.contract_created = True
        return self.env['contract.contract'].create(vals)

    def _catch_values_for_create_contract(self):
        name = _(u"{}: {}").format(self.name, self.partner_id.name)
        vals = {'name': name,
                'partner_id': self.partner_id.id}
        return vals

    @api.multi
    def action_view_contracts(self):
        self.ensure_one()
        action = self.env.ref("contract.action_customer_contract")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [("id", "in", self.mapped('contract_ids').ids)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict
