# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    student_id = fields.Many2one(
        string='Student', comodel_name='res.partner')
    education_center_id = fields.Many2one(
        string='Education center', related='student_id.education_center_id',
        comodel_name='res.partner', store=True)
    event_id = fields.Many2one(
        string='Event', comodel_name='event.event')
