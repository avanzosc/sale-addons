# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    sale_order_ids = fields.Many2many(
        string='Sale orders', comodel_name='sale.order',
        compute='_compute_sale_order_ids', store=True)
    count_sale_orders = fields.Integer(
        string='# Sale orders', compute='_compute_count_sale_orders')

    @api.depends('contract_line_ids', 'contract_line_ids.sale_order_line_id')
    def _compute_sale_order_ids(self):
        for contract in self:
            lines = contract.contract_line_ids.filtered(
                lambda x: x.sale_order_line_id)
            sale_orders = lines.mapped('sale_order_line_id.order_id')
            if sale_orders:
                contract.sale_order_ids = [(6, 0, sale_orders.ids)]

    def _compute_count_sale_orders(self):
        for contract in self:
            contract.count_sale_orders = len(contract.sale_order_ids)

    def action_view_sale_orders(self):
        self.ensure_one()
        return {
            'view_type': 'form',
            'view_mode': 'tree,kanban,form,calendar,pivot,graph,activity',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref(
                'sale.sale_order_view_search_inherit_sale').id,
            'domain': "[('id','in',{})]".format(
                self.mapped('sale_order_ids').ids),
            'context': self.env.context
            }
