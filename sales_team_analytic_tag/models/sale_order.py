# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    analytic_tag_ids = fields.Many2many(
        comodel_name='account.analytic.tag',
        )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        for line in lines:
            line.analytic_tag_ids = list(
                dict.fromkeys(line.analytic_tag_ids.ids +
                              line.order_id.team_id.analytic_tag_ids.ids))
        return lines
