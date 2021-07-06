
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        self.partner_id.create_validate_bank_account_mandate()
        return super(SaleOrder, self)._action_confirm()
