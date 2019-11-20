# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child',
        domain=[('educational_category', '=', 'student')])
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')])

    @api.multi
    def action_confirm(self):
        for sale in self:
            lines = sale.mapped('order_line').filtered(
                lambda x: x.total_percentage != 100.0)
            if lines:
                raise ValidationError(
                    _('The payers do not add 100%'))
        return super(SaleOrder, self).action_confirm()
