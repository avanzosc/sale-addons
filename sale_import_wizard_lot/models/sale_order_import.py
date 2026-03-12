# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models

from odoo.addons.base_import_wizard.models.base_import import convert2str


class SaleOrderImport(models.Model):
    _inherit = "sale.order.import"

    def _get_line_values(self, row_values, datemode=False):
        self.ensure_one()
        values = super()._get_line_values(row_values, datemode=datemode)
        if row_values:
            lot_name = row_values.get("Lote", "")
            values.update(
                {
                    "lot_name": convert2str(lot_name),
                }
            )
        return values
