# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    opportunity_id = fields.Many2one(
        comodel_name='crm.lead', string='Opportunity')
    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child',
        domain=[('educational_category', '=', 'student')])
    course_id = fields.Many2one(
        comodel_name='education.course', string='Initial school course')
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')])
    academic_year_id = fields.Many2one(
        comodel_name='education.academic_year', string='Academic year')

    @api.multi
    def action_confirm(self):
        for sale in self:
            lines = sale.mapped('order_line').filtered(
                lambda x: x.total_percentage != 100.0)
            if lines:
                raise ValidationError(
                    _('The payers do not add 100%'))

        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    originator_id = fields.Many2one(
        comodel_name='res.company', string='Originator')
    payer_ids = fields.One2many(
        comodel_name='sale.order.line.payer', string='Payers',
        inverse_name='line_id')
    total_percentage = fields.Float(
        string='Total Percentage', compute='_compute_total_percentage',
        store=True)

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


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    course_id = fields.Many2one(
        comodel_name='education.course', string='Initial school course')
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')])
