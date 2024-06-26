from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    error_bank_acc = fields.Boolean(
        string="Bank account error", related="partner_id.error_bank_acc"
    )

    def _action_confirm(self):
        if self.payment_mode_id.payment_method_id.mandate_required:
            self.partner_id.create_validate_bank_account_mandate()
        return super(SaleOrder, self)._action_confirm()
