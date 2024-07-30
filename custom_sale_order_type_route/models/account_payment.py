# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_signed = fields.Monetary(
        compute="_compute_amount_signed",
        string="Amount",
        store=True,
    )

    @api.depends("payment_type", "amount")
    def _compute_amount_signed(self):
        for payment in self:
            amount_signed = payment.amount
            if payment.payment_type == "outbound":
                amount_signed = payment.amount * (-1)
            payment.amount_signed = amount_signed
