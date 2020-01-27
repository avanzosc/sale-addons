# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _find_payer_mandates(self):
        self.ensure_one()
        mandates = self.env["account.banking.mandate"]
        for payer in self.payer_ids:
            mandates |= payer._find_mandate()
        return mandates

    @api.multi
    def _generate_sepa_mandate(self):
        for payer in self.mapped('payer_ids'):
            payer._find_or_create_mandate()
