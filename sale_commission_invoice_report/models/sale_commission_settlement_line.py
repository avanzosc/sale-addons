# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SettlementLine(models.Model):
    _inherit = "sale.commission.settlement.line"

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        store=True,
        related="invoice_line_id.move_id",
        string="Source invoice",
    )
