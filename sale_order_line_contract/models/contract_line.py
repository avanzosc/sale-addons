# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class ContractLine(models.Model):
    _inherit = 'contract.line'

    sale_order_line_id = fields.Many2one(
        string='Sale line', comodel_name='sale.order.line')
    sale_order_id = fields.Many2one(
        string='Sale order', comodel_name='sale.order',
        related='sale_order_line_id.order_id', store=True)

    @api.model
    def create(self, vals):
        line = super(ContractLine, self).create(vals)
        if 'no_update_sale_line' not in self.env.context:
            if (line.sale_order_line_id and
                (not line.sale_order_line_id.contract_line_id or
                    line.sale_order_line_id.contract_line_id.id != line.id)):
                line.sale_order_line_id.with_context(
                    no_update_contract_line=True).write(
                        {'contract_line_id': line.id})
        return line

    def write(self, vals):
        result = super(ContractLine, self).write(vals)
        if ('no_update_sale_line' not in self.env.context and
            'sale_order_line_id' in vals and
                vals.get('sale_order_line_id', False)):
            for line in self:
                if (line.sale_order_line_id and
                    (not line.sale_order_line_id.contract_line_id or
                     line.sale_order_line_id.contract_line_id.id != line.id)):
                    line.sale_order_line_id.with_context(
                        no_update_contract_line=True).write(
                            {'contract_line_id': line.id})
        return result
