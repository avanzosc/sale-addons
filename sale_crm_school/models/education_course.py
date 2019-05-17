# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EducationCourse(models.Model):
    _inherit = 'education.course'

    sale_order_template_id = fields.Many2one(
        comodel_name='sale.order.template', string='Quotation template')
