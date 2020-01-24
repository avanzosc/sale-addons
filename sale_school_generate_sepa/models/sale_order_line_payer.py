# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLinePayer(models.Model):
    _inherit = "sale.order.line.payer"

    @api.multi
    def _find_or_create_mandate(self):
        self.ensure_one()
        bank = self._find_payer_bank()
        mandate = self._find_mandate(bank=bank)
        if bank and not mandate:
            wiz_obj = self.env["res.partner.bank.mandate.generator"]
            mandate_wiz = wiz_obj.create({
                "bank_ids": [(6, 0, bank.ids)],
                "mandate_format": "sepa",
                "mandate_type": "recurrent",
                "mandate_scheme": "CORE",
                "mandate_recurrent_sequence_type": "recurring",
                "signed": True,
                "validate": True,
            })
            mandate_wiz.button_generate_mandates()
        elif bank and mandate:
            if not mandate.signature_date:
                mandate.signature_date = fields.Date.context_today(self)
            if mandate.state == "draft":
                mandate.validate()

    @api.multi
    def _find_mandate(self, bank=False):
        self.ensure_one()
        if not bank:
            bank = self._find_payer_bank()
        mandates = bank.mandate_ids.filtered(lambda m: m.state == "valid")
        if not mandates:
            mandates = (
                bank.mandate_ids.sorted("signature_date", reverse=True)
                .filtered(lambda m: m.state == "draft"))
        return mandates and mandates[:1]

    @api.multi
    def _find_payer_bank(self):
        family_rel = self.env["res.partner.family"].search([
            ("child2_id", "=", self.child_id.id),
            ("responsible_id", "=", self.payer_id.id),
            ("family_id", "=", self.line_id.order_id.partner_id.id),
        ])
        bank = (family_rel.bank_id or
                self.payer_id.mapped("bank_ids").filtered("use_default"))
        return bank
