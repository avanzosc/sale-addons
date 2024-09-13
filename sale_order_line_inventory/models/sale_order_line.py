# Copyright 2020 Alfredo de la  Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def show_product_inventory(self):
        self.ensure_one()
        return self.product_id.action_open_quants()
