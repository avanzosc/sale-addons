# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


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
    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child',
        related='line_id.order_id.child_id')
    allowed_payers_ids = fields.Many2many(
        string='Allowed payers', comodel_name='res.partner',
        compute='_compute_allowed_payer_ids')

    @api.multi
    @api.depends('child_id', 'child_id.child2_ids',
                 'child_id.child2_ids.payer',
                 'child_id.child2_ids.responsible_id')
    def _compute_allowed_payer_ids(self):
        for line in self:
            possible_payers = line.child_id.child2_ids.filtered(
                lambda f: f.payer)
            line.allowed_payers_ids = [
                (6, 0, possible_payers.mapped('responsible_id').ids)]

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
