# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrderOption(models.Model):
    _inherit = "sale.order.option"

    @api.multi
    def _get_values_to_add_to_order(self):
        self.ensure_one()
        line_dict = super(SaleOrderOption, self)._get_values_to_add_to_order()
        line_dict.update({
            "payer_ids": self.order_id.child_id.get_payers_info(),
        })
        return line_dict
