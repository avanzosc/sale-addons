# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    contract_line_id = fields.Many2one(
        string='Contract line', comodel_name='contract.line')

    def _create_contract_line(self, contract):
        vals = self._catch_values_for_contract_line()
        vals['contract_id'] = contract.id
        return self.env['contract.line'].create(vals)

    def _catch_values_for_contract_line(self):
        vals = {
            'product_id': self.product_id.id,
            'uom_id': self.product_uom.id,
            'name': self.name,
            'quantity': self.product_uom_qty,
            'price_unit': self.price_unit,
            'recurring_interval': self.product_id.recurring_interval,
            'recurring_rule_type': self.product_id.recurring_rule_type,
            'date_start': fields.Date.context_today(self),
            'recurring_next_date': fields.Date.context_today(self),
            'sale_order_line_id': self.id}
        if self.product_id.apply_recurrence_in != 'contract':
            vals.update(
                {'recurring_rule_type': self.product_id.recurring_rule_type,
                 'recurring_interval': self.product_id.recurring_interval})
        return vals

    @api.model
    def create(self, vals):
        line = super(SaleOrderLine, self).create(vals)
        if ('no_update_contract_line' not in self.env.context and
            line.contract_line_id and
            (not line.contract_line_id.sale_order_line_id or
                line.contract_line_id.sale_order_line_id.id != line.id)):
            line.contract_line_id.with_context(no_update_sale_line=True).write(
                {'sale_order_line_id': line.id})
        return line

    def write(self, vals):
        result = super(SaleOrderLine, self).write(vals)
        if ('no_update_contract_line' not in self.env.context and
            'contract_line_id' in vals and
                vals.get('contract_line_id', False)):
            for line in self:
                if (line.contract_line_id and
                    (not line.contract_line_id.sale_order_line_id or
                     line.contract_line_id.sale_order_line_id.id !=
                        line.id)):
                    line.contract_line_id.with_context(
                        no_update_sale_line=True).write(
                            {'sale_order_line_id': line.id})
        return result
