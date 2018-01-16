# Copyright 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class SaleOrderCondition(models.Model):
    _name = 'sale.order.condition'
    _inherit = ['order.condition']
    _description = 'Sale Order Condition'
    _order = 'condition_id, sale_id'

    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale Order', required=True)
