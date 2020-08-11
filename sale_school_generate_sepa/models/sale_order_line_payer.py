# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLinePayer(models.Model):
    _inherit = "sale.order.line.payer"

    @api.multi
    def check_payment_mode_mandate_required(self):
        self.ensure_one()
        payment_mode = self.payer_id.sudo().with_context(
            force_company=self.originator_id.id).customer_payment_mode_id
        return payment_mode.payment_method_id.mandate_required

    @api.multi
    def _find_or_create_mandate(self):
        self.ensure_one()
        if not self.check_payment_mode_mandate_required():
            return False
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
        return self.bank_id._find_mandate(self.line_id.originator_id)
