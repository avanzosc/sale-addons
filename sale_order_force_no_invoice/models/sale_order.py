# Copyright 2026 AvanzOSC - Lucía Echevarría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    force_no_invoice = fields.Boolean(
        string="Force Nothing to Invoice",
        help="If checked, the order's invoice status is forced to "
        "'Nothing to Invoice' even if there are lines or quantities "
        "still pending invoicing.",
    )

    @api.depends("force_no_invoice")
    def _compute_invoice_status(self):
        super()._compute_invoice_status()
        for order in self:
            if order.force_no_invoice:
                order.invoice_status = "no"
