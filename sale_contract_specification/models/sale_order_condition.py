# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import api, fields, models


class SaleDraftCondition(models.Model):
    _name = 'sale.draft.condition'
    _inherit = ['order.condition']
    _description = 'Draft Sale Order Condition'
    _order = 'condition_id, sale_id'

    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale Order', required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        results = []
        for record in self:
            super(SaleDraftCondition, record).name_get()
            results.append(
                (record.id, '[{}] {}'.format(record.sale_id.name,
                                             record.condition_id.name)))
        return results


class SaleOrderCondition(models.Model):
    _name = 'sale.order.condition'
    _inherit = ['order.condition']
    _description = 'Sale Order Condition'
    _order = 'condition_id, sale_id'

    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale Order', required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        results = []
        for record in self:
            super(SaleOrderCondition, record).name_get()
            results.append(
                (record.id, '[{}] {}'.format(record.sale_id.name,
                                             record.condition_id.name)))
        return results
