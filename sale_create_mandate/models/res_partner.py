
from odoo import models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def create_validate_bank_account_mandate(self):
        if self.bank_ids:
            bank_id = self.env['res.partner.bank'].search(
                [('id', 'in', self.bank_ids.ids)], order='id desc', limit=1)
            if bank_id:
                if bank_id.acc_type not in 'iban':
                    raise ValidationError(
                        _("The order could not be confirmed because "
                          "the customer does not have a valid bank account."))
                else:
                    if not bank_id.mandate_ids:
                        bank_id.create_validate_bank_account_mandate()
        else:
            raise ValidationError("The customer does not have a bank account.")


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def create_validate_bank_account_mandate(self):
        wiz_obj = self.sudo().env["res.partner.bank.mandate.generator"]
        mandate_wiz = wiz_obj.create({
            "bank_ids": [self.id],
            "mandate_format": "sepa",
            "mandate_type": "recurrent",
            "mandate_scheme": "CORE",
            "mandate_recurrent_sequence_type": "recurring",
            "signed": True,
            "validate": True,
        })
        mandate_wiz.button_generate_mandates()
