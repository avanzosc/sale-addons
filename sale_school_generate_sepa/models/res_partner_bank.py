# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    @api.multi
    def _find_mandate(self, originator):
        self.ensure_one()
        bank_mandates = (
            self.mandate_ids.filtered(
                lambda m: m.company_id == originator).sorted(
                "signature_date", reverse=True))
        mandates = bank_mandates.filtered(lambda m: m.state == "valid")
        if not mandates:
            mandates = bank_mandates.filtered(lambda m: m.state == "draft")
        return mandates and mandates[:1] or self.env["account.banking.mandate"]
