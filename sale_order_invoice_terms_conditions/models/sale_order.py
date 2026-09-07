# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        transfering_sale_terms_conditions = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "sale_order_invoice_terms_conditions.transfering_sale_terms_conditions"
            )
            == "True"
        )
        values = super()._prepare_invoice()
        if not transfering_sale_terms_conditions:
            values.pop("narration")
        return values
