# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    originator_id = fields.Many2one(
        comodel_name='res.company', string='Originator')
    center_id = fields.Many2one(
        comodel_name='res.partner', string='Center',
        domain=[('educational_category', '=', 'school')])
