from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _onchange_commitment_date(self):
        res = super()._onchange_commitment_date()

        if isinstance(res, dict):
            res.pop("warning", None)

        return res
