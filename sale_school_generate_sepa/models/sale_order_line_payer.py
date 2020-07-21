# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLinePayer(models.Model):
    _inherit = "sale.order.line.payer"

    @api.multi
    def _find_or_create_mandate(self):
        self.ensure_one()
        mandate = self.sudo()._find_mandate()
        if not mandate:
            wiz_obj = self.sudo().env["res.partner.bank.mandate.generator"]
            mandate_wiz = wiz_obj.with_context(
                force_company=self.line_id.originator_id.id).create({
                    "bank_ids": [(6, 0, self.bank_id.ids)],
                    "mandate_format": "sepa",
                    "mandate_type": "recurrent",
                    "mandate_scheme": "CORE",
                    "mandate_recurrent_sequence_type": "recurring",
                    "signed": True,
                    "validate": True,
                })
            mandate_wiz.button_generate_mandates()
        else:
            if not mandate.signature_date:
                mandate.signature_date = fields.Date.context_today(self)
            if mandate.state == "draft":
                mandate.validate()

    @api.multi
    def _find_mandate(self):
        self.ensure_one()
        bank_mandates = (
            self.bank_id.mandate_ids.sorted("signature_date", reverse=True)
            .filtered(lambda m: m.company_id == self.line_id.originator_id))
        mandates = bank_mandates.filtered(lambda m: m.state == "valid")
        if not mandates:
            mandates = bank_mandates.filtered(lambda m: m.state == "draft")
        return mandates and mandates[:1]
