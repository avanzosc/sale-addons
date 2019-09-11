# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    account_banking_mandate_ids = fields.One2many(
        comodel_name='account.banking.mandate',
        inverse_name='sale_order_id', string='Account banking mandate')
    sepa_count = fields.Integer(
        string="# SEPA", compute='_compute_sepa_count')

    @api.multi
    def _compute_sepa_count(self):
        for sale in self:
            sale.sepa_count = (len(sale.account_banking_mandate_ids))

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            lines = sale.mapped('order_line').filtered(
                lambda x: x.originator_id and x.payer_ids)
            for line in lines:
                line._generate_sepa_mandate()
        return res

    def action_view_sepa_from_sale_order(self):
        self.ensure_one()
        action = self.env.ref(
            'account_banking_mandate.mandate_action').read()[0]
        action['domain'] = [
            ('sale_order_id', '=', self.id)]
        return action


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _generate_sepa_mandate(self):
        mandate_obj = self.env['account.banking.mandate']
        for payer in self.mapped('payer_ids').filtered(
                lambda x: x.payer_id and x.payer_id.bank_ids):
            bank = ((payer.payer_id.mapped('bank_ids').filtered(
                lambda x: x.use_default)) or (payer.payer_id.bank_ids[0]))
            cond = [('company_id', '=', self.originator_id.id),
                    ('partner_id', '=', payer.id),
                    ('state', 'not in', ('expired', 'cancel'))]
            mandate = mandate_obj.search(cond, limit=1)
            if not mandate:
                vals = self._prepare_vals_for_create_sepa(payer, bank)
                mandate = mandate_obj.create(vals)
            if mandate.state == 'draft':
                mandate.validate()

    def _prepare_vals_for_create_sepa(self, payer, bank):
        vals = {
            'sale_order_id': self.order_id.id,
            'company_id': self.originator_id.id,
            'format': 'sepa',
            'type': 'recurrent',
            'partner_bank_id': bank.id,
            'partner_id': payer.id,
            'scheme': 'CORE',
            'recurrent_sequence_type': 'recurring',
            'signature_date':
            fields.Date.to_string(fields.Date.context_today(self))}
        return vals
