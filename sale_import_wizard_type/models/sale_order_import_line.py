# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    def _sale_order_values(self):
        values = super()._sale_order_values()
        if self.import_id.type_id:
            values["type_id"] = self.import_id.type_id.id
        return values
