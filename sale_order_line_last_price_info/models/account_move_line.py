# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_date = fields.Date(
        string="Invoice/Bill Date",
        related="move_id.invoice_date",
        store=True,
        copy=False,
    )
