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

    @api.onchange('child_id')
    def onchange_child_id(self):
        for line in self:
            payers = []
            if line.child_id:
                families = line.child_id.child2_ids.filtered(lambda c: c.payer)
                payers = families.mapped('responsible_id')
            line.allowed_payers_ids = (
                [(6, 0, payers.ids)] if payers else [(6, 0, [])])

    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child')
    allowed_payers_ids = fields.Many2many(
        string='Allowed payers', comodel_name='res.partner',
        relation='rel_sale_order_line_payers', column1='sale_order_line_id',
        column2='sale_order_line_payer_id')
