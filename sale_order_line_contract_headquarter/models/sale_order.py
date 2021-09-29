# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _catch_values_for_create_contract(self, line):
        vals = super(SaleOrder, self)._catch_values_for_create_contract(line)
        if self.headquarter_id:
            vals['headquarter_id'] = self.headquarter_id.id
        return vals
