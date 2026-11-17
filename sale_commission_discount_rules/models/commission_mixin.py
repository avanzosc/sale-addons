# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import operator

from odoo import api, models

OPERATORS = {
    "==": operator.eq,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
}


class CommissionLineMixin(models.AbstractModel):
    _inherit = "commission.line.mixin"

    @api.model
    def _get_formula_input_dict(self):
        return {
            "line": self.object_id,
            "self": self,
        }

    def _get_commission_amount(self, commission, subtotal, product, quantity):
        """Get the commission amount for the data given. To be called by
        compute methods of children models.
        """
        self.ensure_one()
        if (
            not product.commission_free
            and commission
            and commission.commission_type == "filter"
        ):
            formulas = commission.formula_data_ids

            if formulas:
                for f in formulas:
                    if OPERATORS[f.operation](self.object_id.discount, f.discount):
                        return (self.object_id.price_subtotal * f.commission) / 100
            else:
                return 0

        return super()._get_commission_amount(commission, subtotal, product, quantity)
