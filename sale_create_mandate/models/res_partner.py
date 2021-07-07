
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    error_bank_acc = fields.Boolean(
        string='Bank account error',
        compute="_compute_partner_validate_bank_account")

    @api.depends('bank_ids')
    def _compute_partner_validate_bank_account(self):
        for record in self:
            record.error_bank_acc = False
            if not record.bank_ids or True in record.bank_ids.mapped(
                    'error_bank_acc'):
                record.error_bank_acc = True

    def create_validate_bank_account_mandate(self):
        if self.bank_ids:
            bank_id = self.env['res.partner.bank'].search(
                [('id', 'in', self.bank_ids.ids)], order='id desc', limit=1)
            if bank_id:
                if bank_id.error_bank_acc:
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

    error_bank_acc = fields.Boolean(
        string='Bank account error',
        compute="_compute_validate_bank_account")

    @api.depends('acc_type')
    def _compute_validate_bank_account(self):
        for record in self:
            record.error_bank_acc = False
            if record.acc_type not in 'iban':
                record.error_bank_acc = True

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
