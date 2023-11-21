# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderImportLine(models.Model):
    _inherit = "sale.order.import.line"

    def _create_sale_order(self):
        sale_order = super(SaleOrderImportLine, self)._create_sale_order()
        sale_order._compute_sale_type_id()
        return sale_order
