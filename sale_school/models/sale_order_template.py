# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')],
        copy=False)
    course_id = fields.Many2one(
        comodel_name='education.course', string='Course',
        copy=False)

    _sql_constraints = [
        ('school_course_unique', 'unique(school_id, course_id)',
         'Template must be unique per school and course!'),
    ]
