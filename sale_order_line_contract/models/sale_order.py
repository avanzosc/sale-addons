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
    contract_created = fields.Integer(
        string='Contract created', default=0)
    contract_modified = fields.Integer(
        string='Contract modified', default=0)
    contract_created_literal = fields.Text(
        string='Contract created literal')

    @api.depends('order_line', 'order_line.contract_line_id')
    def _compute_contract_ids(self):
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.contract_line_id)
            contracts = lines.mapped('contract_line_id.contract_id')
            if contracts:
                sale.contract_ids = [(6, 0, contracts.ids)]

    def _compute_count_contracts(self):
        for sale in self:
            sale.count_contracts = len(sale.contract_ids)

    def _action_confirm(self):
        message1 = _('CONTRACT(s) CREATED')
        message2 = _('CONTRACT(s) HAVE BEEN MODIFIED {} TIMES.')
        res = super(SaleOrder, self)._action_confirm()
        for sale in self:
            lines = sale.catch_lines_to_try()
            if lines:
                sale.create_contract_lines(lines)
                lit = ""
                if sale.contract_created:
                    lit = '{}: {}'.format(message1, sale.contract_created)
                if sale.contract_modified:
                    lit_message2 = message2.format(sale.contract_modified)
                    _('CONTRACT(s) HAVE BEEN MODIFIED {} TIMES.')
                    lit = lit_message2 if not lit else '{}\n{}'.format(
                        lit, lit_message2)
                if lit:
                    sale.contract_created_literal = lit
        return res

    def catch_lines_to_try(self):
        lines = self.order_line.filtered(
            lambda x: x.product_id and x.product_id.recurring_rule_type)
        return lines

    def create_contract_lines(self, lines):
        for line in lines:
            cond = [('partner_id', '=', self.partner_id.id),
                    ('contract_type', '=', 'sale'),
                    '|', ('date_end', '=', False),
                    ('date_end', '>', fields.Date.context_today(self))]
            if line.product_id.apply_recurrence_in == 'contract':
                cond.append(('line_recurrence', '=', False))
            else:
                cond.append(('line_recurrence', '=', True))
            contract = self.env['contract.contract'].search(cond, limit=1)
            if contract:
                self.contract_modified = self.contract_modified + 1
            if not contract:
                contract = self.create_contract(line)
                contract._onchange_partner_id()
            line.contract_line_id = line._create_contract_line(contract).id

    def create_contract(self, line):
        vals = self._catch_values_for_create_contract(line)
        self.contract_created = self.contract_created + 1
        return self.env['contract.contract'].create(vals)

    def _catch_values_for_create_contract(self, line):
        name = _(u"{}: {}").format(self.name, self.partner_id.name)
        vals = {'name': name,
                'partner_id': self.partner_id.id,
                'line_recurrence': True}
        if line.product_id.apply_recurrence_in == 'contract':
            vals.update(
                {'line_recurrence': False,
                 'recurring_rule_type': line.product_id.recurring_rule_type,
                 'recurring_interval': line.product_id.recurring_interval})
        return vals

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
