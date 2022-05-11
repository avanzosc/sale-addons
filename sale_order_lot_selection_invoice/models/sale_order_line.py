# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        result = super(SaleOrderLine, self)._prepare_invoice_line(
            **optional_values)
        if self.lot_id:
            result['name'] = _(u"{} - lot: {}").format(
                self.name, self.lot_id.name)
        return result
