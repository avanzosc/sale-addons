# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class AccountBankingMandate(models.Model):
    _inherit = 'account.banking.mandate'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')
