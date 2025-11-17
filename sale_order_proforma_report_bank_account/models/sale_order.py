# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def partner_banks_to_show(self):
        self.ensure_one()
        if self.payment_mode_id.show_bank_account_from_journal:
            if self.payment_mode_id.bank_account_link == "fixed":
                return self.payment_mode_id.fixed_journal_id.bank_account_id
            else:
                return self.payment_mode_id.variable_journal_ids.mapped(
                    "bank_account_id"
                )
        if (
            self.payment_mode_id.payment_method_id.code == "sepa_direct_debit"
        ):  # pragma: no cover
            return self.partner_id.valid_mandate_id.partner_bank_id
        # Return this as empty recordset
        return self.env["res.partner.bank"]
