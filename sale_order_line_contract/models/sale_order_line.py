# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


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
            'name': self.name,
            'quantity': self.product_uom_qty,
            'price_unit': self.price_unit,
            'recurring_interval': self.product_id.recurring_interval,
            'recurring_rule_type': self.product_id.recurring_rule_type,
            'date_start': fields.Date.context_today(self),
            'recurring_next_date': fields.Date.context_today(self)}
        return vals
