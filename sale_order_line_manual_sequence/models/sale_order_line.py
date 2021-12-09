# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = "order_id, manual_sequence, id"

    manual_sequence = fields.Char(
        string='Manual seq.')

    def _prepare_invoice_line(self):
        self.ensure_one()
        result = super(SaleOrderLine, self)._prepare_invoice_line()
        result['manual_sequence'] = self.manual_sequence
        return result
