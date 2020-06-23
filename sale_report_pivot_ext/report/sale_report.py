# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = 'sale.report'

    commitment_date = fields.Date(
        string='Commitment Date', readonly=True)

    def _query(self, with_clause='', fields=None, groupby='', from_clause=''):
        if not fields:
            fields = {}
        fields["commitment_date"] = ', s.commitment_date as commitment_date'
        groupby += ', s.commitment_date'
        return super(SaleReport, self)._query(
            with_clause=with_clause, fields=fields, groupby=groupby,
            from_clause=from_clause)
