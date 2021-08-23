# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    def button_add_to_order(self):
        result = super(SaleOrderOption, self).button_add_to_order()
        if self.line_id:
            result2 = self.line_id.product_id_change()
            if result2 and 'warning' in result2:
                return result2
        return result
