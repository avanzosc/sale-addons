# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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

    total_percentage = fields.Float(store=True)
    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child')


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')])
    course_id = fields.Many2one(
        comodel_name='education.course', string='Course')


class SaleOrderTemplateLine(models.Model):
    _inherit = "sale.order.template.line"

    company_id = fields.Many2one(
        string='Company', comodel_name='res.company',
        related='product_id.company_id', store=True)


class SaleOrderLinePayer(models.Model):
    _inherit = "sale.order.line.payer"

    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child', required=True)
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
