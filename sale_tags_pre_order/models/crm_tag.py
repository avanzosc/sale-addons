# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CRMTag(models.Model):
    _inherit = "crm.tag"

    is_pre_order = fields.Boolean()
    invoice_mode = fields.Selection(
        selection=[
            ("none", "None"),
            ("open", "Open"),
            ("paid", "Paid"),
        ],
        default="none",
    )
    journal_id = fields.Many2one(
        string="Advance Journal",
        comodel_name="account.journal",
    )
