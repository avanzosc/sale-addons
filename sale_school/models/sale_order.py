# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    originator_id = fields.Many2one(
        comodel_name='res.company', string='Originator',
        related='product_id.company_id', store=True)
    payer_id = fields.Many2one(
        comodel_name='res.partner', string='Payer')
    payer_ids = fields.One2many(
        comodel_name='sale.order.line.payer', string='Payers',
        inverse_name='line_id')
    total_percentage = fields.Float(
        string='Total Percentage', compute='_compute_total_percentage')

    @api.depends('payer_ids', 'payer_ids.pay_percentage')
    def _compute_total_percentage(self):
        for record in self:
            record.total_percentage = sum(record.mapped(
                'payer_ids.pay_percentage')) if record.payer_ids else 100.0


class SaleOrderLinePayer(models.Model):
    _name = 'sale.order.line.payer'
    _description = 'Payer per Sale Line'
    _rec_name = 'payer_id'

    line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale Line', required=True,
        ondelete='cascade')
    payer_id = fields.Many2one(
        comodel_name='res.partner', string='Payer', required=True)
    pay_percentage = fields.Float(string='Percentage', required=True)

    @api.multi
    def name_get(self):
        """ name_get() -> [(id, name), ...]

        Returns a textual representation for the records in ``self``.
        By default this is the value of the ``display_name`` field.

        :return: list of pairs ``(id, text_repr)`` for each records
        :rtype: list(tuple)
        """
        result = []
        for record in self:
            result.append((record.id, '{} ({} %)'.format(
                record.payer_id.name, record.pay_percentage)))
        return result
