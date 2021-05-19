# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, _


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

    @api.model
    def create(self, vals):
        if 'product_tmpl_id' in vals and vals.get('product_tmpl_id', False):
            template = self.env['product.template'].browse(
                vals.get('product_tmpl_id'))
            if template.product_variant_count == 0:
                vals.update({
                    'recurring_rule_type': template.recurring_rule_type,
                    'recurring_interval': template.recurring_interval,
                    'apply_recurrence_in': template.apply_recurrence_in})
        product = super(ProductProduct, self).create(vals)
        if 'product_tmpl_id' not in vals:
            if product.product_tmpl_id.product_variant_count == 1:
                product.product_tmpl_id.write({
                    'recurring_rule_type': product.recurring_rule_type,
                    'recurring_interval': product.recurring_interval,
                    'apply_recurrence_in': product.apply_recurrence_in})
        return product

    def write(self, vals):
        result = super(ProductProduct, self).write(vals)
        if ('no_update_template' not in self.env.context and
            ('recurring_interval' in vals or 'recurring_rule_type' in vals or
                'apply_recurrence_in' in vals)):
            for product in self:
                if product.product_tmpl_id.product_variant_count == 1:
                    template = product.product_tmpl_id
                    template_vals = {
                        'recurring_interval': product.recurring_interval,
                        'recurring_rule_type': product.recurring_rule_type,
                        'apply_recurrence_in': product.apply_recurrence_in}
                    template.with_context(
                        no_update_product=True).write(template_vals)
        return result
