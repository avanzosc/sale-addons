# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_default_tag(self):
        sale_obj = self.env['sale.order']
        context_data = self.env.context.get('params', {})
        tag_ids = {}
        if 'model' in context_data and context_data['model'] == 'sale.order':
            sale = sale_obj.browse(context_data['id'])
            tag_ids = sale.team_id.analytic_tag_ids.ids
        return tag_ids

    analytic_tag_ids = fields.Many2many(
        comodel_name='account.analytic.tag',
        default=lambda self: self._get_default_tag())
