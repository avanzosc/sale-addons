
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    error_bank_acc = fields.Boolean(
        string='Bank account error',
        related="partner_id.error_bank_acc")

    def _action_confirm(self):
        self.partner_id.create_validate_bank_account_mandate()
        return super(SaleOrder, self)._action_confirm()
