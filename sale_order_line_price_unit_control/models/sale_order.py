# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError
from odoo.tools import config


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if config["test_enable"] and not self.env.context.get("check_amount_less"):
            return super().action_confirm()
        for sale in self:
            min_price_unit = sale._get_min_price_unit()
            lines = sale.order_line.filtered(
                lambda x, min_price_unit=min_price_unit: x.price_unit == min_price_unit
            )
            if lines:
                raise UserError(
                    _(
                        "You have  %(num_lines)s with an amount less than or "
                        "equal to %(price_unit)s."
                    )
                    % {"num_lines": len(lines), "price_unit": min_price_unit}
                )
        return super().action_confirm()

    def _get_min_price_unit(self):
        return 1
