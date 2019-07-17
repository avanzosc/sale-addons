# Copyright 2019 Daniel Campos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    center_id = fields.Many2one(
        comodel_name='res.partner', string='Center',
        domain=[('educational_category', '=', 'school')])
