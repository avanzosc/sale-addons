# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class SaleConditionTemplate(models.Model):
    _name = 'sale.condition.template'
    _description = 'Sale Conditions Template'
    _inherit = ['mail.thread']

    name = fields.Char(string='Title', translate=True, required=True)
    condition_ids = fields.Many2many(
        comodel_name='sale.condition', string='Conditions',
        relation='rel_condition_template', column1='template_id',
        column2='condition_id')
