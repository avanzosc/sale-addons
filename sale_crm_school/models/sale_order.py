# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    course_id = fields.Many2one(
        comodel_name='education.course', string='Initial school course')
    academic_year_id = fields.Many2one(
        comodel_name='education.academic_year', string='Academic year')


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
