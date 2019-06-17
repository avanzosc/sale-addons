# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EducationCourse(models.Model):
    _inherit = 'education.course'

    sale_order_template_ids = fields.One2many(
        comodel_name='sale.order.template', string='Quotation templates',
        inverse_name='course_id')
    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template', string='Quotation template',
        compute='_compute_sale_order_template_id', store=True)

    @api.depends('sale_order_template_ids')
    def _compute_sale_order_template_id(self):
        for course in self.filtered(lambda c: c.sale_order_template_ids):
            course.sale_order_template_id = (
                course.sale_order_template_ids[0].id)
