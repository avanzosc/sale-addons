# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    condition_tmpl_id = fields.Many2one(
        comodel_name='sale.condition.template',
        string='Specification Template', copy=False, readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    condition_ids = fields.One2many(
        comodel_name='sale.order.condition', inverse_name='sale_id',
        string='Sale Conditions', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    @api.onchange('condition_tmpl_id')
    def _onchange_condition_tmpl_id(self):
        if self.condition_tmpl_id:
            condition_ids = [
                (0, 0, {'condition_id': x.condition_id.id,
                        'description': x.description})
                for x in self.condition_ids]
            condition_ids += [
                (0, 0, {'condition_id': x.id,
                        'description': x.description or x.name})
                for x in self.condition_tmpl_id.condition_ids]
            self.condition_ids = condition_ids