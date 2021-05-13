# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    recurring_interval = fields.Integer(
        string='Invoice Every', default=0)
    recurring_rule_type = fields.Selection(
        [('daily', _('Day(s)')),
         ('weekly', _('Week(s)')),
         ('monthly', _('Month(s)')),
         ('monthlylastday', _('Month(s) last day')),
         ('quarterly', _('Quarter(s)')),
         ('semesterly', _('Semester(s)')),
         ('yearly', _('Year(s)'))],
        string='Recurrence')
    apply_recurrence_in = fields.Selection(
        [('contract', _('Contract')),
         ('line', _('Contract line'))],
        string='Apply recurrence in')
